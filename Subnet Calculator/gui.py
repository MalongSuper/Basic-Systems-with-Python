#!/usr/bin/env python3
"""Tkinter GUI for the IPv4 subnet calculator modules in subnets/."""

from __future__ import annotations

import struct
import sys
import zlib
from ipaddress import IPv4Network
from pathlib import Path
from tkinter import filedialog, messagebox, ttk
import tkinter as tk

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "subnets"))

from address import ExtendedAddress  # noqa: E402
from borrowed_hosts import borrowed_bits, usable_subnets as borrowed_usable  # noqa: E402
from subnet_mask_network import IPAddress  # noqa: E402
from network_class import default_prefix, network_address  # noqa: E402
from subnetting_network import subnetting_plan  # noqa: E402
from usable_hosts import host_bits, subnet_bits, usable_hosts  # noqa: E402
from usable_hosts import usable_subnets as count_usable_subnets  # noqa: E402


APP_TITLE = "IPv4 Subnet Calculator"
PAD = {"padx": 10, "pady": 6}


def parse_octets(text: str) -> tuple[int, int, int, int]:
    parts = [p.strip() for p in text.replace(",", ".").split(".")]
    if len(parts) != 4:
        raise ValueError("Enter an IPv4 address as n1.n2.n3.n4")
    octets = [int(p) for p in parts]
    if any(o < 0 or o > 255 for o in octets):
        raise ValueError("Each octet must be between 0 and 255")
    return octets[0], octets[1], octets[2], octets[3]


def parse_cidr(text: str) -> int:
    raw = text.strip().lstrip("/")
    cidr = int(raw)
    if cidr < 0 or cidr > 32:
        raise ValueError("CIDR must be between 0 and 32")
    return cidr


def dotted_to_binary(dotted: str) -> str:
    return " ".join(f"{int(octet):08b}" for octet in dotted.split("."))


def first_last_from_network(network_dotted: str, broadcast_dotted: str) -> tuple[str, str]:
    net = [int(x) for x in network_dotted.split(".")]
    bcast = [int(x) for x in broadcast_dotted.split(".")]
    net_int = (net[0] << 24) + (net[1] << 16) + (net[2] << 8) + net[3]
    bcast_int = (bcast[0] << 24) + (bcast[1] << 16) + (bcast[2] << 8) + bcast[3]
    if bcast_int - net_int < 2:
        return network_dotted, broadcast_dotted

    def to_dotted(value: int) -> str:
        return ".".join(str((value >> shift) & 255) for shift in (24, 16, 8, 0))

    return to_dotted(net_int + 1), to_dotted(bcast_int - 1)


def labeled_entry(parent, label: str, width: int = 22) -> tuple[ttk.Frame, ttk.Entry]:
    frame = ttk.Frame(parent)
    ttk.Label(frame, text=label).pack(anchor="w")
    entry = ttk.Entry(frame, width=width)
    entry.pack(fill="x", pady=(2, 0))
    return frame, entry


class ResultTable(ttk.Frame):
    def __init__(self, parent, columns: list[tuple[str, str, int]]):
        super().__init__(parent)
        ids = [c[0] for c in columns]
        self.tree = ttk.Treeview(self, columns=ids, show="headings", height=12)
        for col_id, heading, width in columns:
            self.tree.heading(col_id, text=heading)
            self.tree.column(col_id, width=width, anchor="w")
        scroll = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

    def set_rows(self, rows: list[tuple]):
        self.tree.delete(*self.tree.get_children())
        for row in rows:
            self.tree.insert("", "end", values=row)


class IPv4Tab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        form = ttk.LabelFrame(self, text="Address")
        form.pack(fill="x", **PAD)
        ip_box, self.ip_entry = labeled_entry(form, "IPv4 address")
        cidr_box, self.cidr_entry = labeled_entry(form, "CIDR prefix", width=8)
        ip_box.pack(side="left", padx=(8, 8), pady=8)
        cidr_box.pack(side="left", padx=(8, 8), pady=8)
        self.ip_entry.insert(0, "192.168.1.10")
        self.cidr_entry.insert(0, "24")
        ttk.Button(form, text="Compute", command=self.compute).pack(side="left", padx=8, pady=18)

        self.table = ResultTable(
            self,
            [
                ("field", "Field", 220),
                ("decimal", "Decimal", 280),
                ("binary", "Binary", 420),
            ],
        )
        self.table.pack(fill="both", expand=True, **PAD)
        self.ip_entry.bind("<Return>", lambda _e: self.compute())
        self.cidr_entry.bind("<Return>", lambda _e: self.compute())

    def compute(self):
        try:
            n1, n2, n3, n4 = parse_octets(self.ip_entry.get())
            cidr = parse_cidr(self.cidr_entry.get())
            ip = ExtendedAddress(n1, n2, n3, n4, cidr)
            klass = network_address(ip) or "Unclassified"
            prefix = default_prefix(ip)
            first, last = first_last_from_network(ip.SubnetDecimal, ip.BroadcastDecimal)
            host_count = usable_hosts(cidr)
            try:
                _network_name, subnet_count = count_usable_subnets(cidr, ip)
                subnet_bit_count = subnet_bits(cidr, ip)
                subnet_note = str(subnet_count)
            except ValueError as exc:
                subnet_count = None
                subnet_bit_count = "—"
                subnet_note = str(exc)

            rows = [
                ("IPv4 / CIDR", ip.Address, ""),
                ("Type", ip.IPType, ""),
                ("Class", klass, ""),
                ("Default class prefix", str(prefix) if prefix is not None else "—", ""),
                ("Host", ip.HostDecimal, ip.HostBinary),
                ("Subnet mask", ip.MaskDecimal, ip.MaskBinary),
                ("Network ID", ip.SubnetDecimal, ip.SubnetBinary),
                ("Broadcast ID", ip.BroadcastDecimal, ip.BroadcastBinary),
                ("First usable", first, dotted_to_binary(first)),
                ("Last usable", last, dotted_to_binary(last)),
                ("Usable hosts", str(host_count), f"2^({32 - cidr}) - 2"),
                ("Host bits", str(host_bits(cidr)), "32 - CIDR"),
                ("Subnet bits", str(subnet_bit_count), "CIDR - default prefix"),
                ("Usable subnets", subnet_note, "" if subnet_count is None else "2^(subnet bits)"),
                ("Valid range", f"{first} – {last}", ""),
            ]
            self.table.set_rows(rows)
        except Exception as exc:
            messagebox.showerror("Invalid input", str(exc))


class CidrTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        toolbar = ttk.Frame(self)
        toolbar.pack(fill="x", **PAD)
        ttk.Label(toolbar, text="CIDR prefix table (/1 – /32)").pack(side="left")
        ttk.Button(toolbar, text="Download PNG", command=self.download_png).pack(side="right")

        self.table = ResultTable(
            self,
            [
                ("cidr", "CIDR", 80),
                ("binary", "Binary mask", 420),
                ("decimal", "Decimal mask", 220),
            ],
        )
        self.table.pack(fill="both", expand=True, **PAD)
        self.rows = []
        for cidr in range(1, 33):
            mask = IPAddress(1, 1, 1, 1, cidr).Mask
            row = (f"/{cidr}", mask[0], mask[1])
            self.rows.append(row)
        self.table.set_rows(self.rows)

    def download_png(self):
        path = filedialog.asksaveasfilename(
            title="Save CIDR table",
            defaultextension=".png",
            filetypes=[("PNG image", "*.png")],
            initialfile="cidr_table.png",
        )
        if not path:
            return
        try:
            save_cidr_png(path, self.rows)
            messagebox.showinfo("Saved", f"CIDR table saved to:\n{path}")
        except Exception as exc:
            messagebox.showerror("Could not save PNG", str(exc))


# 5x7 glyphs for the CIDR table PNG (stdlib-only export).
_FONT_5X7 = {
    " ": ["00000"] * 7,
    ".": ["00000", "00000", "00000", "00000", "00000", "01100", "01100"],
    "/": ["00001", "00010", "00100", "01000", "10000", "00000", "00000"],
    "0": ["01110", "10001", "10011", "10101", "11001", "10001", "01110"],
    "1": ["00100", "01100", "00100", "00100", "00100", "00100", "01110"],
    "2": ["01110", "10001", "00001", "00010", "00100", "01000", "11111"],
    "3": ["11110", "00001", "00001", "01110", "00001", "00001", "11110"],
    "4": ["00010", "00110", "01010", "10010", "11111", "00010", "00010"],
    "5": ["11111", "10000", "11110", "00001", "00001", "10001", "01110"],
    "6": ["01110", "10000", "10000", "11110", "10001", "10001", "01110"],
    "7": ["11111", "00001", "00010", "00100", "01000", "01000", "01000"],
    "8": ["01110", "10001", "10001", "01110", "10001", "10001", "01110"],
    "9": ["01110", "10001", "10001", "01111", "00001", "00001", "01110"],
    "A": ["01110", "10001", "10001", "11111", "10001", "10001", "10001"],
    "B": ["11110", "10001", "10001", "11110", "10001", "10001", "11110"],
    "C": ["01110", "10001", "10000", "10000", "10000", "10001", "01110"],
    "D": ["11100", "10001", "10001", "10001", "10001", "10001", "11100"],
    "E": ["11111", "10000", "10000", "11110", "10000", "10000", "11111"],
    "I": ["01110", "00100", "00100", "00100", "00100", "00100", "01110"],
    "K": ["10001", "10010", "10100", "11000", "10100", "10010", "10001"],
    "L": ["10000", "10000", "10000", "10000", "10000", "10000", "11111"],
    "M": ["10001", "11011", "10101", "10101", "10001", "10001", "10001"],
    "N": ["10001", "11001", "10101", "10011", "10001", "10001", "10001"],
    "O": ["01110", "10001", "10001", "10001", "10001", "10001", "01110"],
    "R": ["11110", "10001", "10001", "11110", "10100", "10010", "10001"],
    "T": ["11111", "00100", "00100", "00100", "00100", "00100", "00100"],
    "W": ["10001", "10001", "10001", "10101", "10101", "10101", "01010"],
    "Y": ["10001", "10001", "01010", "00100", "00100", "00100", "00100"],
}


def _hex_to_rgb(color: str) -> tuple[int, int, int]:
    color = color.lstrip("#")
    return int(color[0:2], 16), int(color[2:4], 16), int(color[4:6], 16)


def _fill_rect(pixels, width, x0, y0, x1, y1, color):
    r, g, b = color
    for y in range(max(0, y0), min(len(pixels), y1)):
        row = pixels[y]
        for x in range(max(0, x0), min(width, x1)):
            i = x * 3
            row[i], row[i + 1], row[i + 2] = r, g, b


def _draw_text(pixels, width, x, y, text, color, scale=2):
    r, g, b = color
    cursor = x
    for char in text.upper():
        glyph = _FONT_5X7.get(char, _FONT_5X7[" "])
        for gy, bits in enumerate(glyph):
            for gx, bit in enumerate(bits):
                if bit != "1":
                    continue
                for sy in range(scale):
                    py = y + gy * scale + sy
                    if py < 0 or py >= len(pixels):
                        continue
                    row = pixels[py]
                    for sx in range(scale):
                        px = cursor + gx * scale + sx
                        if 0 <= px < width:
                            i = px * 3
                            row[i], row[i + 1], row[i + 2] = r, g, b
        cursor += 6 * scale


def _write_png(path: str, pixels: list[bytearray], width: int, height: int):
    raw = b"".join(b"\x00" + bytes(row) for row in pixels)
    ihdr = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)

    def chunk(tag: bytes, data: bytes) -> bytes:
        return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)

    png = b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr) + chunk(b"IDAT", zlib.compress(raw, 9)) + chunk(b"IEND", b"")
    Path(path).write_bytes(png)


def save_cidr_png(path: str, rows: list[tuple[str, str, str]]):
    header = ("CIDR", "BINARY", "DECIMAL")
    padding = 24
    line_h = 26
    col_widths = [90, 470, 200]
    width = padding * 2 + sum(col_widths)
    height = padding * 2 + 44 + line_h * (len(rows) + 1)
    bg = _hex_to_rgb("#0f172a")
    header_bg = _hex_to_rgb("#1e293b")
    odd = _hex_to_rgb("#111827")
    even = _hex_to_rgb("#1f2937")
    text = _hex_to_rgb("#f8fafc")
    accent = _hex_to_rgb("#93c5fd")
    title = _hex_to_rgb("#e2e8f0")

    pixels = [bytearray(width * 3) for _ in range(height)]
    _fill_rect(pixels, width, 0, 0, width, height, bg)
    _draw_text(pixels, width, padding, padding, "CIDR NETWORK TABLE", title, scale=3)

    y = padding + 44
    x = padding
    for i, heading in enumerate(header):
        _fill_rect(pixels, width, x, y, x + col_widths[i], y + line_h, header_bg)
        _draw_text(pixels, width, x + 8, y + 6, heading, accent, scale=2)
        x += col_widths[i]

    for index, row in enumerate(rows):
        y += line_h
        _fill_rect(pixels, width, padding, y, width - padding, y + line_h, odd if index % 2 == 0 else even)
        x = padding
        for i, value in enumerate(row):
            _draw_text(pixels, width, x + 8, y + 6, str(value), text, scale=2)
            x += col_widths[i]

    _write_png(path, pixels, width, height)


class BorrowedTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        form = ttk.LabelFrame(self, text="Borrowed bits")
        form.pack(fill="x", **PAD)

        ttk.Label(form, text="Network class").grid(row=0, column=0, sticky="w", padx=8, pady=8)
        self.class_var = tk.StringVar(value="C")
        ttk.Combobox(
            form,
            textvariable=self.class_var,
            values=("A", "B", "C"),
            state="readonly",
            width=8,
        ).grid(row=0, column=1, padx=8, pady=8)

        ttk.Label(form, text="Required subnets").grid(row=0, column=2, sticky="w", padx=8, pady=8)
        self.subnets_entry = ttk.Entry(form, width=10)
        self.subnets_entry.insert(0, "6")
        self.subnets_entry.grid(row=0, column=3, padx=8, pady=8)
        ttk.Button(form, text="Calculate", command=self.compute).grid(row=0, column=4, padx=8, pady=8)

        self.table = ResultTable(
            self,
            [
                ("field", "Field", 320),
                ("value", "Value", 280),
            ],
        )
        self.table.pack(fill="both", expand=True, **PAD)
        self.subnets_entry.bind("<Return>", lambda _e: self.compute())

    def compute(self):
        try:
            klass = self.class_var.get().upper()
            subnets = int(self.subnets_entry.get().strip())
            bits = borrowed_bits(subnets)
            cidr, usable_subnet_count, hosts_each = borrowed_usable(subnets, klass)
            default = {"A": 8, "B": 16, "C": 24}[klass]
            self.table.set_rows(
                [
                    ("Network class", klass),
                    ("Default prefix", f"/{default}"),
                    ("Borrowed bits (s)", str(bits)),
                    ("New CIDR", f"/{cidr}"),
                    ("Usable number of subnets", str(usable_subnet_count)),
                    ("Usable hosts per subnet", str(hosts_each)),
                    ("Formula", f"CIDR = {default} + {bits}, hosts = 2^({32 - cidr}) - 2"),
                ]
            )
        except Exception as exc:
            messagebox.showerror("Invalid input", str(exc))


class SubnettingTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        form = ttk.LabelFrame(self, text="VLSM subnetting")
        form.pack(fill="x", **PAD)

        ip_box, self.ip_entry = labeled_entry(form, "Network address")
        cidr_box, self.cidr_entry = labeled_entry(form, "CIDR", width=8)
        count_box, self.count_entry = labeled_entry(form, "Number of subnets", width=10)
        ip_box.pack(side="left", padx=8, pady=8)
        cidr_box.pack(side="left", padx=8, pady=8)
        count_box.pack(side="left", padx=8, pady=8)
        self.ip_entry.insert(0, "192.168.10.0")
        self.cidr_entry.insert(0, "24")
        self.count_entry.insert(0, "4")
        ttk.Button(form, text="Build host fields", command=self.rebuild_host_fields).pack(
            side="left", padx=8, pady=18
        )

        self.host_frame = ttk.LabelFrame(self, text="Hosts required per subnet")
        self.host_frame.pack(fill="x", **PAD)
        self.host_entries: list[ttk.Entry] = []
        self.rebuild_host_fields()

        actions = ttk.Frame(self)
        actions.pack(fill="x", padx=10)
        ttk.Button(actions, text="Calculate subnetting", command=self.compute).pack(side="left")

        self.table = ResultTable(
            self,
            [
                ("name", "Subnet", 110),
                ("req", "Requested hosts", 120),
                ("cidr", "CIDR", 70),
                ("network", "Network", 140),
                ("first", "First usable", 140),
                ("last", "Last usable", 140),
                ("broadcast", "Broadcast", 140),
                ("usable", "Usable hosts", 110),
            ],
        )
        self.table.pack(fill="both", expand=True, **PAD)

    def rebuild_host_fields(self):
        for child in self.host_frame.winfo_children():
            child.destroy()
        self.host_entries = []
        try:
            count = int(self.count_entry.get().strip())
            if count < 1 or count > 32:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid input", "Number of subnets must be an integer from 1 to 32")
            return

        defaults = [60, 30, 14, 6] + [10] * 32
        for i in range(count):
            cell = ttk.Frame(self.host_frame)
            cell.pack(side="left", padx=8, pady=8)
            ttk.Label(cell, text=f"Subnet {i + 1}").pack(anchor="w")
            entry = ttk.Entry(cell, width=8)
            entry.insert(0, str(defaults[i]))
            entry.pack()
            self.host_entries.append(entry)

    def compute(self):
        try:
            n1, n2, n3, n4 = parse_octets(self.ip_entry.get())
            cidr = parse_cidr(self.cidr_entry.get())
            if not self.host_entries:
                self.rebuild_host_fields()
            hosts = {}
            for i, entry in enumerate(self.host_entries, start=1):
                value = int(entry.get().strip())
                if value < 1:
                    raise ValueError("Each subnet needs at least 1 host")
                hosts[f"Subnet {i}"] = value
            network = IPv4Network(f"{n1}.{n2}.{n3}.{n4}/{cidr}", strict=False)
            plan = subnetting_plan(network, hosts)
            rows = [
                (
                    row["name"],
                    row["requested_hosts"],
                    f"/{row['cidr']}",
                    row["network"],
                    row["first"],
                    row["last"],
                    row["broadcast"],
                    row["usable"],
                )
                for row in plan
            ]
            self.table.set_rows(rows)
        except Exception as exc:
            messagebox.showerror("Invalid input", str(exc))


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry("1080x720")
        self.minsize(900, 600)

        header = ttk.Frame(self)
        header.pack(fill="x", padx=12, pady=(12, 0))
        ttk.Label(header, text=APP_TITLE, font=("Helvetica", 18, "bold")).pack(anchor="w")
        ttk.Label(
            header,
            text="Analyze IPv4 addresses, CIDR masks, borrowed bits, usable hosts, and VLSM subnetting.",
        ).pack(anchor="w")

        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=12, pady=12)
        notebook.add(IPv4Tab(notebook), text="IPv4 Address")
        notebook.add(CidrTab(notebook), text="CIDR Table")
        notebook.add(BorrowedTab(notebook), text="Borrowed Hosts")
        notebook.add(SubnettingTab(notebook), text="Subnetting")


def main():
    App().mainloop()


if __name__ == "__main__":
    main()
