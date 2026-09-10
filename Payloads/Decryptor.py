import os 
from cryptography.fernet import Fernet # type: ignore

# ================= CONFIGURATION =================
Target_Folder = r"C:\ImportantFiles"
Target_Extension = '.encrypted'
# =================================================

# ================= Getting the encrypted files =================
def Get_Encrypted_Files():
    Encrypted_Files = []
    for file in os.listdir(Target_Folder):
        _, ext = os.path.splitext(file)
        if ext.lower() == Target_Extension:
            Full_Path = os.path.join(Target_Folder,file)
            Encrypted_Files.append(Full_Path)
    return Encrypted_Files
# ===============================================================

# ================= Generating a decryption key =================
def Decryption_Key():
    Key_path = os.path.join(Target_Folder,"README.txt")   
    with open(Key_path + ":Key","rb") as thekey:
        Key = thekey.read()
    return Key
# ==========================================================================

# ================= Decrypting the files  =================
def Files_Decryption(Encrypted_Files,Key):
    Decryption_count = 0 
    for file in Encrypted_Files:
        try:
            with open(file,'rb') as thefile:
                Content = thefile.read()
                decrypted_data = Fernet(Key).decrypt(Content)
            with open(file,'wb') as thefile:
                thefile.write(decrypted_data)
            if file.endswith(Target_Extension):
                Original_File = file[:-len(Target_Extension)]
                os.rename(file,Original_File)
            Decryption_count +=1
        except Exception as e: 
            print(f"[!] Failed to Decrypt {file}:{e}")
    return Decryption_count
# ==================================================================

# ==================== Main Function =======================
def main():
    
    Key = Decryption_Key()

    Encrypted_Files = Get_Encrypted_Files()

    Decryption_count = Files_Decryption(Encrypted_Files,Key)

    print(f"Decrypted Files = {Decryption_count}")
# ===================================================================

if __name__ == "__main__":
    main()
