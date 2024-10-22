import tkinter as tk
from tkinter import filedialog, messagebox, colorchooser
from PIL import Image, ImageTk, ImageDraw
import os
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

class ImageCropperApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Yoshiki's Image Cropper")
        self.style = ttk.Style("darkly")  # モダンなスタイルを適用
        # アプリのアイコンを設定
        self.root.iconbitmap('./icon.ico')
        # icon_image = tk.PhotoImage(file='./icon.png')  # タスクバーのアイコン画像（PNG形式）
        # self.root.iconphoto(True, icon_image)  # 'icon.ico' は任意のアイコンファイルへのパス
        # 初期化
        self.images = []
        self.image_paths = []
        self.crop_box = None
        self.current_image_index = 0
        self.start_x = None
        self.start_y = None
        self.end_x = None
        self.end_y = None
        self.rect_id = None
        self.square_mode = False
        self.save_original = tk.BooleanVar(value=False)
        self.rect_color = "red"  # 矩形の初期カラー

        # 上部コントロールフレーム
        self.control_frame = ttk.Frame(root, padding=10)
        self.control_frame.pack(side=tk.TOP, fill=tk.X)

        # ボタンを追加
        self.load_button = ttk.Button(self.control_frame, text="Load Images", command=self.load_images, bootstyle=PRIMARY)
        self.load_button.grid(row=0, column=0, padx=5, pady=5)

        self.add_button = ttk.Button(self.control_frame, text="Add More Images", command=self.add_images, bootstyle=SECONDARY)
        self.add_button.grid(row=0, column=1, padx=5, pady=5)

        self.square_mode_button = ttk.Button(self.control_frame, text="Square Crop Mode", command=self.toggle_square_mode, bootstyle=INFO)
        self.square_mode_button.grid(row=0, column=2, padx=5, pady=5)

        self.next_button = ttk.Button(self.control_frame, text="Next Image", command=self.next_image, bootstyle=WARNING)
        self.next_button.grid(row=0, column=3, padx=5, pady=5)

        self.save_button = ttk.Button(self.control_frame, text="Save Cropped Images", command=self.save_cropped_images, bootstyle=SUCCESS)
        self.save_button.grid(row=0, column=4, padx=5, pady=5)

        self.refresh_button = ttk.Button(self.control_frame, text="Refresh", command=self.refresh, bootstyle=DANGER)
        self.refresh_button.grid(row=0, column=5, padx=5, pady=5)

        # ラジオボタンを追加して元画像を保存するオプション
        self.save_original_checkbox = ttk.Checkbutton(self.control_frame, text="Save Original Image with Crop", variable=self.save_original)
        self.save_original_checkbox.grid(row=0, column=6, padx=5, pady=5)

        # 矩形の色を選択するボタン
        self.color_button = ttk.Button(self.control_frame, text="Select Rectangle Color", command=self.choose_color, bootstyle=INFO)
        self.color_button.grid(row=0, column=7, padx=5, pady=5)

        # 画像表示用のCanvas
        self.canvas_frame = ttk.Frame(root)
        self.canvas_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        self.canvas = tk.Canvas(self.canvas_frame, cursor="cross", bg="#f0f0f0")
        self.canvas.pack(expand=True, fill=tk.BOTH)

        # マウスイベントのバインド
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

    def load_images(self):
        # ファイル選択ダイアログで複数の画像を選択
        file_paths = filedialog.askopenfilenames(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")])
        if file_paths:
            loaded_images = [Image.open(path) for path in file_paths]
            if self.check_image_resolution(loaded_images):
                self.image_paths = list(file_paths)
                self.images = loaded_images
                self.current_image_index = 0
                self.cropped_images = [None] * len(self.images)
                self.display_image()
            else:
                messagebox.showerror("Error", "All images must have the same resolution.")

    def add_images(self):
        # 追加の画像を選択
        file_paths = filedialog.askopenfilenames(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")])
        if file_paths:
            loaded_images = [Image.open(path) for path in file_paths]
            if self.check_image_resolution(loaded_images, compare_with_existing=True):
                self.image_paths.extend(file_paths)
                self.images.extend(loaded_images)
                self.cropped_images.extend([None] * len(loaded_images))
            else:
                messagebox.showerror("Error", "All images must have the same resolution as the existing images.")

    def check_image_resolution(self, images, compare_with_existing=False):
        # 解像度が全て同じかチェックする
        if compare_with_existing and self.images:
            expected_size = self.images[0].size
        else:
            expected_size = images[0].size
        for img in images:
            if img.size != expected_size:
                return False
        return True

    def display_image(self):
        if self.images:
            # 画像をリサイズしてCanvasに表示（ウィンドウの限界まで拡大）
            image = self.images[self.current_image_index]
            self.original_image = image.copy()
            self.displayed_image = image.copy()
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()
            aspect_ratio = image.width / image.height

            if canvas_width / canvas_height > aspect_ratio:
                new_height = canvas_height
                new_width = int(aspect_ratio * new_height)
            else:
                new_width = canvas_width
                new_height = int(new_width / aspect_ratio)

            self.displayed_image = self.displayed_image.resize((new_width, new_height), Image.LANCZOS)
            self.tk_image = ImageTk.PhotoImage(self.displayed_image)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)

    def toggle_square_mode(self):
        # 正方形モードをトグル
        self.square_mode = not self.square_mode
        mode = "Square" if self.square_mode else "Rectangle"
        self.square_mode_button.config(text=f"{mode} Crop Mode")

    def choose_color(self):
        # 矩形の色を選択
        color_code = colorchooser.askcolor(title="Choose Rectangle Color")[1]
        if color_code:
            self.rect_color = color_code

    def on_button_press(self, event):
        # マウスクリック位置を記録
        self.start_x = event.x
        self.start_y = event.y
        # 既存の矩形があれば削除
        if self.rect_id:
            self.canvas.delete(self.rect_id)
        self.rect_id = None

    def on_mouse_drag(self, event):
        # マウスをドラッグしている間に矩形を描画
        if self.square_mode:
            # 正方形を描画
            side_length = min(abs(event.x - self.start_x), abs(event.y - self.start_y))
            if event.x < self.start_x:
                end_x = self.start_x - side_length
            else:
                end_x = self.start_x + side_length

            if event.y < self.start_y:
                end_y = self.start_y - side_length
            else:
                end_y = self.start_y + side_length
        else:
            # 矩形を描画
            end_x = event.x
            end_y = event.y

        if self.rect_id:
            self.canvas.delete(self.rect_id)
        self.rect_id = self.canvas.create_rectangle(self.start_x, self.start_y, end_x, end_y, outline=self.rect_color)

    def on_button_release(self, event):
        # マウスボタンを離したときにクロップ領域を決定
        if self.square_mode:
            side_length = min(abs(event.x - self.start_x), abs(event.y - self.start_y))
            if event.x < self.start_x:
                self.end_x = self.start_x - side_length
            else:
                self.end_x = self.start_x + side_length

            if event.y < self.start_y:
                self.end_y = self.start_y - side_length
            else:
                self.end_y = self.start_y + side_length
        else:
            self.end_x = event.x
            self.end_y = event.y

        self.crop_box = (min(self.start_x, self.end_x), min(self.start_y, self.end_y), max(self.start_x, self.end_x), max(self.start_y, self.end_y))

        # すべての画像をクロップして保存
        for i, image in enumerate(self.images):
            self.cropped_images[i] = image.crop(self.adjust_crop_box(image.size, self.displayed_image.size))
        self.canvas.delete(self.rect_id)  # クロップ完了後に描画された矩形を削除
        self.rect_id = None
        self.display_cropped_image()

    def adjust_crop_box(self, original_size, displayed_size):
        # キャンバス上のクロップ座標を元の画像のサイズに合わせて調整
        displayed_width, displayed_height = displayed_size
        original_width, original_height = original_size

        scale_x = original_width / displayed_width
        scale_y = original_height / displayed_height

        left = int(self.crop_box[0] * scale_x)
        top = int(self.crop_box[1] * scale_y)
        right = int(self.crop_box[2] * scale_x)
        bottom = int(self.crop_box[3] * scale_y)

        # 元の画像の範囲内に収まるように調整
        left = max(0, min(original_width, left))
        top = max(0, min(original_height, top))
        right = max(0, min(original_width, right))
        bottom = max(0, min(original_height, bottom))

        return (left, top, right, bottom)

    def display_cropped_image(self):
        if self.cropped_images[self.current_image_index]:
            # クロップされた現在の画像を表示
            cropped_image = self.cropped_images[self.current_image_index]
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()
            aspect_ratio = cropped_image.width / cropped_image.height

            if canvas_width / canvas_height > aspect_ratio:
                new_height = canvas_height
                new_width = int(aspect_ratio * new_height)
            else:
                new_width = canvas_width
                new_height = int(new_width / aspect_ratio)

            cropped_image = cropped_image.resize((new_width, new_height), Image.LANCZOS)
            self.tk_image = ImageTk.PhotoImage(cropped_image)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)

    def next_image(self):
        # 次の画像を表示
        if self.images:
            self.current_image_index = (self.current_image_index + 1) % len(self.images)
            self.display_image()

    def save_cropped_images(self):
        if not hasattr(self, 'cropped_images') or not any(self.cropped_images):
            return

        # 保存先のディレクトリを選択
        save_dir = filedialog.askdirectory()
        if save_dir:
            for i, cropped_image in enumerate(self.cropped_images):
                if cropped_image:
                    # 元のファイル名に "_cropped" を追加して保存
                    base_name = os.path.basename(self.image_paths[i])
                    name, ext = os.path.splitext(base_name)
                    save_path = os.path.join(save_dir, f"{name}_cropped{ext}")
                    cropped_image.save(save_path)

                    # オリジナル画像も保存する場合
                    if self.save_original.get():
                        original_with_rect = self.images[i].copy()
                        draw = ImageDraw.Draw(original_with_rect)
                        draw.rectangle(self.adjust_crop_box(self.images[i].size, self.displayed_image.size), outline=self.rect_color, width=3)
                        original_save_path = os.path.join(save_dir, f"{name}_original_with_rectangle{ext}")
                        original_with_rect.save(original_save_path)

    def refresh(self):
        # 初期画面に戻す
        self.current_image_index = 0
        self.crop_box = None
        self.rect_id = None
        self.display_image()

if __name__ == "__main__":
    root = ttk.Window(themename="cosmo")
    app = ImageCropperApp(root)
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.geometry(f"{int(screen_width * 0.8)}x{int(screen_height * 0.8)}")
    root.mainloop()

