# SMS Encoding - Important Note

## ✅ SMS Send Feature Working!

The SMS send feature is fully functional and tested with the SIM7600 modem.

## 📝 How Character Encoding Works

### Messages That Send Immediately (No Prompt)

✅ **Standard ASCII text** - Perfect support, sends without confirmation

```powershell
python -m sim7600 sms send "+123" "Hello World 123!"
# ✅ Sends immediately - no warnings
```

✅ **Basic punctuation and symbols**

```powershell
python -m sim7600 sms send "+123" "Status: OK! Temperature @ 25C."
# ✅ Sends immediately - no warnings
```

### Messages That Show Confirmation Prompt

⚠️ **Accented characters** - Shows warning, converts to base letters

```powershell
python -m sim7600 sms send "+123" "café résumé"
```

**You'll see:**

```
⚠️  WARNING: Your message contains special characters (accents, emoji, etc.)
The SIM7600 modem has limited support for these characters.
Your message may appear corrupted or garbled on the recipient's phone.

Original message: café résumé
May be sent as:     cafe resume

Do you want to continue anyway? (y/N):
```

⚠️ **Messages with emoji** - Shows warning, emoji become `?`

```powershell
python -m sim7600 sms send "+123" "Test 👋🎉"
```

**You'll see:**

```
⚠️  WARNING: Your message contains special characters (accents, emoji, etc.)
The SIM7600 modem has limited support for these characters.
Your message may appear corrupted or garbled on the recipient's phone.

Original message: Test 👋🎉
May be sent as:     Test ??

Do you want to continue anyway? (y/N):
```

## 🔧 Technical Details

### Why GSM Encoding Only?

The SIM7600 modem has limitations:

- **Text mode (AT+CMGF=1)** - Simple but doesn't support full Unicode
- **PDU mode (AT+CMGF=0)** - Would support Unicode but very complex

**Our approach:**

- Use GSM encoding (text mode) for simplicity and reliability
- Warn users when characters will be converted
- Show preview of what will actually be sent
- Let user decide whether to proceed

### Character Conversion Rules

**How it works:**

1. **Unicode Normalization (NFD)** - Decomposes characters
   - Example: `é` → `e` + accent mark
2. **Strip Combining Characters** - Removes accent marks
   - Keeps base letter: `e`
3. **Replace Non-ASCII** - Everything else becomes `?`
   - Example: `🎉` → `?`

**Results:**

```
café résumé    → cafe resume
naïve          → naive
¡Hola!         → ?Hola!
Hello 🎉       → Hello ?
Привет         → ??????
```

## 🎯 Best Practices

### For Best Results

**Use ASCII-only messages:**

```powershell
# Perfect - no issues
python -m sim7600 sms send "+123" "Server backup completed at 3:45 PM"
python -m sim7600 sms send "+123" "Temperature: 25C, Status: OK"
python -m sim7600 sms send "+123" "Alert: Disk space low"
```

### For Accented Languages

**Be aware of conversion:**

```powershell
# Spanish
python -m sim7600 sms send "+123" "Hola! Como estas?"
# Better than: "¡Hola! ¿Cómo estás?" → "?Hola! ?Como estas?"

# French
python -m sim7600 sms send "+123" "Bonjour! Ca va bien?"
# Better than: "Bonjour! Ça va bien?" → "Bonjour! Ca va bien?"
```

### For Emoji

**Consider the trade-off:**

```powershell
# Emoji will become ?
python -m sim7600 sms send "+123" "Congratulations on your achievement! 🎉"
# Recipient sees: "Congratulations on your achievement! ?"

# Better option: Use words
python -m sim7600 sms send "+123" "Congratulations on your achievement!"
```

## 💡 When to Use Special Characters

### ✅ Go ahead if:

- You understand they'll be converted
- The converted message is still meaningful
- Your recipient expects plain text anyway

### ⚠️ Consider alternatives if:

- The accents are essential for meaning
- Emoji are important to your message
- You need exact character preservation

## 🚀 What We Tested

### Successful Tests

✅ **ASCII message** - Sent perfectly

```powershell
python -m sim7600 sms send "+4915140142720" "Test message"
Result: ✅ Sent immediately, received perfectly
```

✅ **Message with emoji** - Sent with confirmation

```powershell
python -m sim7600 sms send "+4915140142720" "Test 👋🎉"
Result: ⚠️ Showed warning, sent as "Test ??"
```

✅ **Accented characters** - Sent with confirmation

```powershell
python -m sim7600 sms send "+4915140142720" "café résumé"
Result: ⚠️ Showed warning, sent as "cafe resume"
```

## ✅ Bottom Line

**The SMS send feature is working perfectly!**

- ✅ ASCII messages: Send immediately, received perfectly
- ⚠️ Special characters: Show warning, user confirms, send successfully
- 🔍 Transparent: You see exactly what will be sent before confirming
- 💪 Reliable: Works consistently with SIM7600 modem

**Use it confidently for:**

- System alerts and notifications
- Status updates
- Error messages
- Any messages where ASCII is sufficient

**Consider the limitations for:**

- Messages where accents are critical
- Emoji-heavy messages
- Non-Latin scripts (Chinese, Arabic, etc.)

---

**Ready to send your first SMS?**

```powershell
# Simple ASCII - sends immediately
python -m sim7600 sms send "+YOUR_NUMBER" "Hello from sim7600!"

# With special chars - shows confirmation
python -m sim7600 sms send "+YOUR_NUMBER" "Test café 🎉"
```

**Note:** The confirmation prompt is a feature, not a bug! It ensures you know exactly what your recipient will see.
