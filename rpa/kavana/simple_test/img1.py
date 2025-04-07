from lib.core.managers.image_manager import ImageManager

def run_image_command(command, **kwargs):
    print(f"\n🔧 실행: {command}")
    manager = ImageManager(command=command, **kwargs)
    manager.execute()

def main():
    base_path = "C:/Users/PC/Pictures/"
    source_file = base_path + "efriend1.png"

    # 1. resize
    run_image_command(
        "resize",
        file=source_file,
        width=300,
        height=200,
        save_as=base_path+"efriend1_300x200.png"
    )

    # 2. clip
    run_image_command(
        "clip",
        file=source_file,
        region=(50, 50, 200, 200),
        save_as=base_path+"efriend1_clipped.png"
    )

    # 3. to_gray
    run_image_command(
        "to_gray",
        file=source_file,
        save_as=base_path+"efriend1_gray.png"
    )

    # 4. convert_to
    run_image_command(
        "convert_to",
        file=source_file,
        format="jpeg",
        save_as=base_path+"efriend1_converted.jpg"
    )

    # 5. rotate
    run_image_command(
        "rotate",
        file=source_file,
        angle=90,
        save_as=base_path+"efriend1__rotated.png"
    )

    # 6. blur
    run_image_command(
        "blur",
        file=source_file,
        radius=4,
        save_as=base_path+"efriend1_blurred.png"
    )

    # 7. threshold (이진화)
    run_image_command(
        "threshold",
        file=source_file,
        level=128,
        save_as=base_path+"efriend1_thresholded.png"
    )

if __name__ == "__main__":
    main()
