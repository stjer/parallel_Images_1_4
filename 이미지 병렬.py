import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from PIL import Image

# 전역 변수로 레이아웃 설정 저장
GLOBAL_LAYOUT_TYPE = None
GLOBAL_GAP = 10

def select_images():
    file_paths = filedialog.askopenfilenames(
        title="Select Images",
        filetypes=[("Image files", "*.png *.jpg *.jpeg")]
    )
    return list(file_paths)

def arrange_images(image_paths, layout_type=None, gap=None):
    global GLOBAL_LAYOUT_TYPE, GLOBAL_GAP

    # 최초 실행 시 레이아웃과 간격 설정
    if layout_type is None:
        layout_type = GLOBAL_LAYOUT_TYPE
    if gap is None:
        gap = GLOBAL_GAP

    # Support 1, 2, 3, 4 image configurations
    if len(image_paths) not in [1, 2, 3, 4]:
        raise ValueError("Only 1, 2, 3, or 4 images supported")

    # Load images and resize to equal dimensions
    images = [Image.open(path) for path in image_paths]
    
    # Find minimum width and height
    min_width = min(img.width for img in images)
    min_height = min(img.height for img in images)
    
    # Resize all images to minimum dimensions
    resized_images = [img.resize((min_width, min_height)) for img in images]
    
    # Create blank images for empty slots
    while len(resized_images) < 4:
        blank_img = Image.new('RGBA', (min_width, min_height), (255, 255, 255, 0))
        resized_images.append(blank_img)
    
    # Calculate total canvas size with gaps
    if len(images) in [1, 2]:
        if layout_type == '2칸 가로':
            grid_width, grid_height = 2, 1
            canvas_width = min_width * grid_width + gap * (grid_width - 1)
            canvas_height = min_height * grid_height + gap * (grid_height - 1)
        else:  # 4칸 정사각형
            grid_width, grid_height = 2, 2
            canvas_width = min_width * grid_width + gap * (grid_width - 1)
            canvas_height = min_height * grid_height + gap * (grid_height - 1)
    else:
        # 3, 4개 이미지는 2x2 그리드
        grid_width, grid_height = 2, 2
        canvas_width = min_width * grid_width + gap * (grid_width - 1)
        canvas_height = min_height * grid_height + gap * (grid_height - 1)
    
    # Create blank canvas
    canvas = Image.new('RGBA', (canvas_width, canvas_height), (255, 255, 255, 0))
    
    # Place images on canvas
    for i in range(4 if len(image_paths) > 2 else 2):
        row = i // grid_width
        col = i % grid_width
        
        x = col * (min_width + gap)
        y = row * (min_height + gap)
        
        canvas.paste(resized_images[i], (x, y))
    
    # Save result
    #print("이미지 저장 경로를 설정합니다.")
    output_path = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("PNG files", "*.png")]
    )
    if output_path:
        canvas.save(output_path)
        #print(f"Image saved to {output_path}")

def choose_initial_settings():
    global GLOBAL_LAYOUT_TYPE, GLOBAL_GAP
    
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    #print("1~4장의 이미지들을 한번에 선택해주세요.")
    # 이미지 선택
    images = select_images()
    
    # 첫 실행 시에만 갭과 레이아웃 설정
    if GLOBAL_GAP == 10:  # 이 부분 추가
        # 갭 설정 대화상자
        gap = simpledialog.askinteger(
            "간격 설정", 
            "이미지 사이의 간격(픽셀)을 입력하세요(0~10000):", 
            initialvalue=10, 
            minvalue=0, 
            maxvalue=10000
        )
        GLOBAL_GAP = gap if gap is not None else 10
    
    # 첫 실행 시에만 레이아웃 설정
    if GLOBAL_LAYOUT_TYPE is None:  # 이 부분 추가
        # 2개 이미지일 경우 레이아웃 선택
        if len(images) in [1, 2]:
            layout = messagebox.askyesno(
                "Layout 선택", 
                "2개의 이미지를 2칸 가로로 배치하시겠습니까?\n" + 
                "(아니오 클릭 시 4칸 정사각형으로 배치됩니다)"
            )
            GLOBAL_LAYOUT_TYPE = '2칸 가로' if layout else '4칸 정사각형'
        else:
            GLOBAL_LAYOUT_TYPE = '4칸 정사각형'
    
    # 이미지 배치
    arrange_images(images)

def main():
    while True:
        choose_initial_settings()
        
        # 계속할지 묻기
        continue_choice = messagebox.askyesno(
            "계속하기", 
            "다른 이미지로 작업을 계속하시겠습니까?"
        )
        
        if not continue_choice:
            break

if __name__ == "__main__":
    main()
