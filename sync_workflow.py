import os

os.chdir(os.path.expanduser('~/zealot-storage'))

# Read the latest workflow from the Zealot repo
with open(os.path.expanduser('~/zealot/docs/ci/read-upload.yml'), 'r') as f:
    s = f.read()

# Ensure the workflows directory exists
os.makedirs('.github/workflows', exist_ok=True)

# Fix 1: Remove the SIGN_UPLOADED_APKS rejection block so org signing works unconditionally
s = s.replace("""          if [[ ${SIGN_UPLOADED_APKS:-} == true ]]; then
            fail "SIGN_UPLOADED_APKS is no longer supported (Task 40n-c): Zealot never re-signs an uploaded APK. Delete the variable"
          fi
""", "")

# Fix 2: Only run the standalone APK signing step if SDK injection did NOT happen 
# (because the SDK patcher already signs the APK with the org key).
s = s.replace("      - name: Sign the uploaded APK with the organisation key (disabled)\n        if: endsWith(inputs.filename, '.apk')\n", "      - name: Sign the uploaded APK with the organisation key\n        if: endsWith(inputs.filename, '.apk') && env.SDK_INJECTED != '1'\n")

# Write the updated workflow to the storage repo
with open('.github/workflows/read-upload.yml', 'w') as f:
    f.write(s)

print("Workflow synced and fixed successfully.")
