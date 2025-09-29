import os
import sys # Import the sys module to access command-line arguments
from PIL import Image

def convert_pngs_to_jpg_in_folder(source_dir, output_dir=None, quality=95):
    """
    Converts all PNG files in the specified source_dir to JPG and saves them 
    in an optional output directory or a default location with a '-jpg' suffix.

    Args:
        source_dir (str): The path to the folder containing the PNG files.
        output_dir (str, optional): The path to save the resulting JPG files. 
                                    If None, a directory named '<source_dir>-jpg' 
                                    is created alongside the source_dir.
                                    Defaults to None.
        quality (int): The JPG quality level (1-100). Defaults to 95.
    """
    
    # 1. Validate the source directory
    if not os.path.isdir(source_dir):
        print(f"❌ Error: Source directory not found at: {os.path.abspath(source_dir)}")
        return

    # 2. Determine and prepare the output directory
    if output_dir is None:
        # 📌 MODIFICATION: Set the default output folder to <source_dir>-jpg
        output_dir = source_dir + "-jpg"
    
    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"Starting PNG to JPG conversion from: {os.path.abspath(source_dir)}")
    print(f"Outputting JPG files to: {os.path.abspath(output_dir)}")
    print(f"JPG Quality: {quality}\n")

    conversion_count = 0
    
    # 3. Loop through all items in the source directory
    for item in os.listdir(source_dir):
        # Check if the item is a file AND its name ends with '.png'
        # The .py file is correctly skipped here as its extension is not .png
        if item.lower().endswith('.png') and os.path.isfile(os.path.join(source_dir, item)):
            
            # Full path to the input PNG file
            png_path = os.path.join(source_dir, item)
            
            # Create the new JPG filename
            jpg_filename = os.path.splitext(item)[0] + '.jpg'
            jpg_path = os.path.join(output_dir, jpg_filename)
            
            try:
                # Open the PNG image
                img = Image.open(png_path)
                
                # Convert to 'RGB' to handle potential PNG transparency before saving as JPG
                # JPG does not support transparency.
                rgb_img = img.convert('RGB')
                
                # Save as JPG
                rgb_img.save(jpg_path, 'JPEG', quality=quality)
                
                conversion_count += 1
                print(f"   - Converted: {item}")
                
            except Exception as e:
                print(f"   ❌ ERROR converting {item}: {e}")

    # 4. Final summary
    print(f"\n✅ Conversion complete. Successfully processed {conversion_count} PNG file(s).")


# --- Configuration and Execution ---

# Set the JPG quality (95 is high quality)
JPG_QUALITY = 95

if __name__ == "__main__":
    # Check if a directory path was passed as a command-line argument
    if len(sys.argv) < 2:
        print("\n\n---------------------------------------------------------")
        print("🔴 Usage Error: Please provide the target folder path.")
        print("Example: python script_name.py /path/to/your/images/folder")
        print("---------------------------------------------------------")
        # Exit the script with an error code
        sys.exit(1)
        
    # sys.argv[0] is the script name; sys.argv[1] is the first argument (the folder path)
    TARGET_FOLDER_PATH = sys.argv[1]
    
    # Optional: If a second argument is provided, use it as the output path.
    # If this is None, the function will use the default '-jpg' naming convention.
    OUTPUT_PATH = sys.argv[2] if len(sys.argv) > 2 else None

    convert_pngs_to_jpg_in_folder(TARGET_FOLDER_PATH, OUTPUT_PATH, JPG_QUALITY)