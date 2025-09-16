# Apple Shortcuts Setup Guide for iPhone iMessage

## 🍎 **Complete Setup Guide**

### **Step 1: Generate Sample Data**

First, let's create sample data for testing:

```bash
python3 src/apple_shortcuts.py
```

This creates two files:
- `shortcuts/shortcuts_sample.json` - Sample data for testing
- `shortcuts/shortcuts_real.json` - Real results from your league

### **Step 2: Transfer Data to iPhone**

**Option A: AirDrop (Recommended)**
1. Open AirDrop on your Mac
2. Drag `shortcuts/shortcuts_sample.json` to your iPhone
3. Accept the file on your iPhone

**Option B: Email**
1. Email `shortcuts/shortcuts_sample.json` to yourself
2. Open email on iPhone and save attachment

**Option C: iCloud Drive**
1. Copy file to iCloud Drive
2. Access from iPhone Files app

### **Step 3: Create Apple Shortcut**

#### **3.1 Open Shortcuts App**
- Find "Shortcuts" app on your iPhone
- Tap the "+" button to create new shortcut

#### **3.2 Add Actions**

**Action 1: Get Contents of File**
1. Search for "Get Contents of File"
2. Add this action
3. Tap "Choose File" and select `shortcuts/shortcuts_sample.json`

**Action 2: Get Value from Input**
1. Search for "Get Value from Input"
2. Add this action
3. Set Key to "message_text"
4. Set Input to "Contents of File"

**Action 3: Send Message**
1. Search for "Send Message"
2. Add this action
3. Set Message to "Value from Input"
4. Set Recipients to your group chat
5. Make sure "Send Immediately" is OFF (so you can review)

#### **3.3 Configure Shortcut**
1. Tap the shortcut name at the top
2. Rename to "Skins Game Results"
3. Choose an icon (🏈 football emoji)
4. Tap "Done"

### **Step 4: Test the Shortcut**

1. **Run the shortcut** by tapping it
2. **Review the message** before sending
3. **Send to your group chat**
4. **Verify it appears correctly**

### **Step 5: Update for Real Data**

Once testing works with sample data:

1. **Generate real data**: `python3 src/apple_shortcuts.py`
2. **Transfer `shortcuts/shortcuts_real.json`** to your iPhone
3. **Update shortcut** to use real data file
4. **Test with real results**

---

## 📱 **Shortcut Workflow**

### **Weekly Process:**
1. **Process week**: `python3 main.py` (processes previous week)
2. **Generate data**: `python3 src/apple_shortcuts.py`
3. **Transfer file** to iPhone
4. **Run shortcut** on iPhone
5. **Send to group chat**

### **Automated Process (Advanced):**
You can create a more advanced shortcut that:
1. Downloads the file from iCloud Drive automatically
2. Processes the latest results
3. Sends immediately (or with confirmation)

---

## 🔧 **Troubleshooting**

### **Common Issues:**

**"File not found"**
- Make sure file is in iPhone Files app
- Check file name matches exactly

**"No data in file"**
- Run `python3 src/apple_shortcuts.py` again
- Check that results exist in your league

**"Message too long"**
- Shortcuts has message length limits
- Consider splitting into multiple messages

**"Group chat not found"**
- Make sure group chat is saved in Contacts
- Use phone number instead of name

### **Testing Steps:**

1. **Test with sample data first**
2. **Test with your personal number**
3. **Test with group chat**
4. **Verify message formatting**

---

## 💡 **Pro Tips**

### **Message Formatting:**
- Keep messages concise for group chats
- Use emojis sparingly (they take up characters)
- Test message length before sending

### **File Management:**
- Keep both sample and real files on iPhone
- Update real file weekly
- Use sample file for testing changes

### **Shortcut Optimization:**
- Add confirmation step to prevent accidental sends
- Use "Ask Each Time" for recipients
- Add error handling for missing files

---

## 🚀 **Next Steps**

1. **Generate sample data**: `python3 src/apple_shortcuts.py`
2. **Transfer to iPhone** via AirDrop
3. **Create shortcut** following steps above
4. **Test with sample data**
5. **Update for real data** when ready

**Ready to set up your Apple Shortcut?**
