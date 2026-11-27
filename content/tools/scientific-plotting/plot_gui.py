"""plot_style / plot_utils を使った簡易グラフ作成GUI。

ヘッダなしCSVから列番号を指定して複数系列を重ね描きし、軸ラベル・範囲・
対数/線形スケール・凡例位置を画面上で調整しながらプレビューし、PNGとして
保存できる。CLIでスクリプトを毎回書き換えずに済ませたい、簡単な確認用途を
想定した最小限の実装(twinx・カテゴリ軸など、元にした描画スクリプト群の一部機能は非対応)。
"""

from __future__ import annotations

import tkinter as tk
from dataclasses import dataclass
from tkinter import filedialog, messagebox, ttk

from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from plot_style import apply_style
from plot_utils import new_figure, read_column

COLOR_CHOICES = [
    "red",
    "blue",
    "green",
    "black",
    "orange",
    "purple",
    "Cyan",
    "Magenta",
]
LINESTYLE_CHOICES = ["solid", "dashed", "dotted", "dashdot"]
YSCALE_CHOICES = ["linear", "log"]
LEGEND_LOC_CHOICES = [
    "best",
    "upper right",
    "upper left",
    "lower left",
    "lower right",
]


@dataclass
class SeriesSpec:
    x_col: int
    y_col: int
    label: str
    color: str = "red"
    linestyle: str = "solid"
    y_scale: float = 1.0

    def summary(self) -> str:
        return (
            f"x={self.x_col} y={self.y_col} label={self.label!r} "
            f"color={self.color} style={self.linestyle} yscale*{self.y_scale}"
        )


class PlotGuiApp:
    """plot_utils を使った簡易グラフ作成GUIのメインウィンドウ。"""

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        root.title("plot_utils 簡易グラフ作成GUI")

        self.csv_path: str = ""
        self.series: list[SeriesSpec] = []
        self.fig = None

        self._build_widgets()

    # ------------------------------------------------------------------
    # ウィジェット構築
    # ------------------------------------------------------------------
    def _build_widgets(self) -> None:
        left = ttk.Frame(self.root, padding=8)
        left.grid(row=0, column=0, sticky="nsw")
        right = ttk.Frame(self.root, padding=8)
        right.grid(row=0, column=1, sticky="nsew")
        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(0, weight=1)

        self._build_csv_section(left)
        self._build_series_section(left)
        self._build_axis_section(left)
        self._build_action_section(left)
        self._build_canvas_section(right)

    def _build_csv_section(self, parent: ttk.Frame) -> None:
        frame = ttk.LabelFrame(parent, text="CSVファイル", padding=6)
        frame.pack(fill="x", pady=4)

        self.csv_path_var = tk.StringVar(value="(未選択)")
        ttk.Label(frame, textvariable=self.csv_path_var, width=40).pack(
            side="left", fill="x", expand=True
        )
        ttk.Button(frame, text="参照...", command=self._on_browse_csv).pack(
            side="left", padx=4
        )

    def _build_series_section(self, parent: ttk.Frame) -> None:
        frame = ttk.LabelFrame(parent, text="系列", padding=6)
        frame.pack(fill="x", pady=4)

        form = ttk.Frame(frame)
        form.pack(fill="x")

        self.x_col_var = tk.StringVar(value="0")
        self.y_col_var = tk.StringVar(value="1")
        self.label_var = tk.StringVar(value="series")
        self.color_var = tk.StringVar(value=COLOR_CHOICES[0])
        self.linestyle_var = tk.StringVar(value=LINESTYLE_CHOICES[0])
        self.yscale_mult_var = tk.StringVar(value="1.0")

        ttk.Label(form, text="X列").grid(row=0, column=0, sticky="w")
        ttk.Entry(form, textvariable=self.x_col_var, width=6).grid(row=0, column=1)
        ttk.Label(form, text="Y列").grid(row=0, column=2, sticky="w")
        ttk.Entry(form, textvariable=self.y_col_var, width=6).grid(row=0, column=3)

        ttk.Label(form, text="ラベル").grid(row=1, column=0, sticky="w")
        ttk.Entry(form, textvariable=self.label_var, width=16).grid(
            row=1, column=1, columnspan=3, sticky="we"
        )

        ttk.Label(form, text="色").grid(row=2, column=0, sticky="w")
        ttk.Combobox(
            form, textvariable=self.color_var, values=COLOR_CHOICES, width=8
        ).grid(row=2, column=1)
        ttk.Label(form, text="線種").grid(row=2, column=2, sticky="w")
        ttk.Combobox(
            form, textvariable=self.linestyle_var, values=LINESTYLE_CHOICES, width=8
        ).grid(row=2, column=3)

        ttk.Label(form, text="Y倍率").grid(row=3, column=0, sticky="w")
        ttk.Entry(form, textvariable=self.yscale_mult_var, width=8).grid(
            row=3, column=1
        )

        ttk.Button(form, text="系列を追加", command=self._on_add_series).grid(
            row=3, column=3, sticky="e"
        )

        self.series_listbox = tk.Listbox(frame, height=5)
        self.series_listbox.pack(fill="x", pady=4)
        ttk.Button(
            frame, text="選択した系列を削除", command=self._on_remove_series
        ).pack(anchor="e")

    def _build_axis_section(self, parent: ttk.Frame) -> None:
        frame = ttk.LabelFrame(parent, text="軸・凡例設定", padding=6)
        frame.pack(fill="x", pady=4)

        self.title_var = tk.StringVar(value="")
        self.xlabel_var = tk.StringVar(value="Voltage (V)")
        self.ylabel_var = tk.StringVar(value="Current (A)")
        self.xlim_min_var = tk.StringVar(value="")
        self.xlim_max_var = tk.StringVar(value="")
        self.ylim_min_var = tk.StringVar(value="")
        self.ylim_max_var = tk.StringVar(value="")
        self.yscale_var = tk.StringVar(value=YSCALE_CHOICES[0])
        self.legend_loc_var = tk.StringVar(value=LEGEND_LOC_CHOICES[0])
        self.tick_labelsize_var = tk.StringVar(value="12")

        ttk.Label(frame, text="タイトル").grid(row=0, column=0, sticky="w")
        ttk.Entry(frame, textvariable=self.title_var, width=24).grid(
            row=0, column=1, columnspan=3, sticky="we"
        )

        ttk.Label(frame, text="Xラベル").grid(row=1, column=0, sticky="w")
        ttk.Entry(frame, textvariable=self.xlabel_var, width=24).grid(
            row=1, column=1, columnspan=3, sticky="we"
        )
        ttk.Label(frame, text="Yラベル").grid(row=2, column=0, sticky="w")
        ttk.Entry(frame, textvariable=self.ylabel_var, width=24).grid(
            row=2, column=1, columnspan=3, sticky="we"
        )

        ttk.Label(frame, text="X範囲").grid(row=3, column=0, sticky="w")
        ttk.Entry(frame, textvariable=self.xlim_min_var, width=8).grid(row=3, column=1)
        ttk.Entry(frame, textvariable=self.xlim_max_var, width=8).grid(row=3, column=2)

        ttk.Label(frame, text="Y範囲").grid(row=4, column=0, sticky="w")
        ttk.Entry(frame, textvariable=self.ylim_min_var, width=8).grid(row=4, column=1)
        ttk.Entry(frame, textvariable=self.ylim_max_var, width=8).grid(row=4, column=2)

        ttk.Label(frame, text="Yスケール").grid(row=5, column=0, sticky="w")
        ttk.Combobox(
            frame, textvariable=self.yscale_var, values=YSCALE_CHOICES, width=8
        ).grid(row=5, column=1)

        ttk.Label(frame, text="凡例位置").grid(row=6, column=0, sticky="w")
        ttk.Combobox(
            frame,
            textvariable=self.legend_loc_var,
            values=LEGEND_LOC_CHOICES,
            width=12,
        ).grid(row=6, column=1, columnspan=2, sticky="w")

        ttk.Label(frame, text="目盛りラベルサイズ").grid(row=7, column=0, sticky="w")
        ttk.Entry(frame, textvariable=self.tick_labelsize_var, width=8).grid(
            row=7, column=1
        )

    def _build_action_section(self, parent: ttk.Frame) -> None:
        frame = ttk.Frame(parent, padding=6)
        frame.pack(fill="x", pady=4)
        ttk.Button(frame, text="プレビュー", command=self._on_preview).pack(
            side="left", padx=2
        )
        ttk.Button(frame, text="PNG保存...", command=self._on_save_png).pack(
            side="left", padx=2
        )
        self.status_var = tk.StringVar(value="")
        ttk.Label(parent, textvariable=self.status_var, foreground="red").pack(fill="x")

    def _build_canvas_section(self, parent: ttk.Frame) -> None:
        self.canvas_frame = parent

    # ------------------------------------------------------------------
    # イベントハンドラ
    # ------------------------------------------------------------------
    def _on_browse_csv(self) -> None:
        path = filedialog.askopenfilename(
            title="CSVファイルを選択",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
        )
        if path:
            self.csv_path = path
            self.csv_path_var.set(path)

    def _on_add_series(self) -> None:
        try:
            x_col = int(self.x_col_var.get())
            y_col = int(self.y_col_var.get())
            y_scale = float(self.yscale_mult_var.get())
        except ValueError:
            messagebox.showerror(
                "入力エラー", "X列・Y列は整数、Y倍率は数値で指定してください。"
            )
            return

        spec = SeriesSpec(
            x_col=x_col,
            y_col=y_col,
            label=self.label_var.get() or f"y{y_col}",
            color=self.color_var.get(),
            linestyle=self.linestyle_var.get(),
            y_scale=y_scale,
        )
        self.series.append(spec)
        self.series_listbox.insert(tk.END, spec.summary())

    def _on_remove_series(self) -> None:
        selection = self.series_listbox.curselection()
        for index in reversed(selection):
            self.series_listbox.delete(index)
            del self.series[index]

    def _parse_float(self, value: str) -> float | None:
        value = value.strip()
        return float(value) if value else None

    def _build_figure(self):
        if not self.csv_path:
            raise ValueError("CSVファイルが選択されていません。")
        if not self.series:
            raise ValueError("系列が1つも追加されていません。")

        tick_labelsize = int(self.tick_labelsize_var.get())
        apply_style(tick_labelsize=tick_labelsize)

        if self.fig is not None:
            plt.close(self.fig)
        fig, ax = new_figure()
        self.fig = fig

        for spec in self.series:
            df_x = read_column(self.csv_path, spec.x_col)
            df_y = read_column(self.csv_path, spec.y_col) * spec.y_scale
            ax.plot(
                df_x,
                df_y,
                label=spec.label,
                color=spec.color,
                linestyle=spec.linestyle,
            )

        if self.title_var.get():
            ax.set_title(self.title_var.get())
        ax.set_xlabel(self.xlabel_var.get(), fontsize=18)
        ax.set_ylabel(self.ylabel_var.get(), fontsize=18)

        xlim_min = self._parse_float(self.xlim_min_var.get())
        xlim_max = self._parse_float(self.xlim_max_var.get())
        if xlim_min is not None and xlim_max is not None:
            ax.set_xlim(xlim_min, xlim_max)

        ylim_min = self._parse_float(self.ylim_min_var.get())
        ylim_max = self._parse_float(self.ylim_max_var.get())
        if ylim_min is not None and ylim_max is not None:
            ax.set_ylim(ylim_min, ylim_max)

        ax.set_yscale(self.yscale_var.get())
        ax.legend(loc=self.legend_loc_var.get())
        fig.tight_layout()
        return fig

    def _on_preview(self) -> None:
        self.status_var.set("")
        try:
            fig = self._build_figure()
        except Exception as exc:
            self.status_var.set(str(exc))
            messagebox.showerror("プレビューエラー", str(exc))
            return

        for child in self.canvas_frame.winfo_children():
            child.destroy()
        canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def _on_save_png(self) -> None:
        try:
            fig = self._build_figure()
        except Exception as exc:
            messagebox.showerror("保存エラー", str(exc))
            return

        path = filedialog.asksaveasfilename(
            title="PNGとして保存",
            defaultextension=".png",
            filetypes=[("PNG files", "*.png")],
        )
        if not path:
            return
        fig.savefig(path, format="png", dpi=300)
        messagebox.showinfo("保存完了", f"{path} に保存しました。")


def main() -> None:
    root = tk.Tk()
    PlotGuiApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
