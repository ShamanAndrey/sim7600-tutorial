# 🚀 Migration Guide: `sms_logger` → `sim7600`

## What Changed?

The project has been renamed from `sms_logger` to `sim7600` to better reflect its expanded scope:
- ✅ **SMS** - Currently working
- 🚧 **GPS** - Coming soon
- 🚧 **Voice** - Coming soon

## Quick Migration

### Old Command ❌
```powershell
python -m sms_logger
```

### New Command ✅
```powershell
python -m sim7600 sms receive
```

## Complete Command Mapping

| Old Command | New Command |
|------------|-------------|
| `python -m sms_logger` | `python -m sim7600 sms receive` |
| `python -m sms_logger --init-only` | `python -m sim7600 sms receive --init-only` |
| `python -m sms_logger --port COM10` | `python -m sim7600 sms receive --port COM10` |
| `python -m sms_logger --no-console` | `python -m sim7600 sms receive --no-console` |
| `python -m sms_logger --json-out file.jsonl` | `python -m sim7600 sms receive --json-out file.jsonl` |

## If You Had Scripts

### Before ❌
```python
from sms_logger.modem import Modem
from sms_logger.parser import parse_cmt_header
```

### After ✅
```python
from sim7600.modem import Modem
from sim7600.parser import parse_cmt_header
```

## New CLI Structure

The new CLI is organized by feature with subcommands:

```powershell
# Main help
python -m sim7600 --help

# SMS operations
python -m sim7600 sms --help
python -m sim7600 sms receive          # ✅ Working now
python -m sim7600 sms send "+123:Hi"   # 🚧 Coming soon

# GPS operations  
python -m sim7600 gps --help           # 🚧 Coming soon
python -m sim7600 gps track

# Voice operations
python -m sim7600 voice --help         # 🚧 Coming soon
python -m sim7600 voice dial "+123"
```

## Why the Change?

### Problems with `sms_logger`
- ❌ Too narrow - only covers SMS receiving
- ❌ Doesn't hint at GPS or voice capabilities
- ❌ Not scalable for multi-feature development

### Benefits of `sim7600`
- ✅ **Hardware-focused** - Names the actual device
- ✅ **Expandable** - Works for all modem features
- ✅ **Professional** - Sounds like a real toolkit
- ✅ **Simple** - Easy to type and remember
- ✅ **Beginner-friendly** - Not intimidating

## What's New?

### 1. Multi-Feature Architecture
The CLI now supports subcommands for different features:
- `sms` - SMS operations (receive, send)
- `gps` - GPS tracking (coming soon)
- `voice` - Voice calls (coming soon)

### 2. Future-Ready Structure
```
sim7600/
├── modem.py        # Core modem communication (shared)
├── parser.py       # Message parsing (shared)
├── cli.py          # Current SMS receive logic
├── __main__.py     # New CLI dispatcher
└── logger_config.py # Logging setup (shared)
```

### 3. Clean Subcommand System
Each feature has its own namespace:
```powershell
sim7600 sms receive    # SMS receiving
sim7600 sms send       # SMS sending (future)
sim7600 gps track      # GPS tracking (future)
sim7600 voice dial     # Voice calls (future)
```

## Do I Need to Reinstall?

**Yes!** Run this once:

```powershell
pip install -e .
```

This updates the package name from `sms_logger` to `sim7600`.

## Troubleshooting

### "No module named sim7600"
Run `pip install -e .` in the project directory.

### "No module named sms_logger"
Perfect! That's expected. The package is now `sim7600`.

### Old scripts not working?
Just change the import:
- Old: `from sms_logger import ...`
- New: `from sim7600 import ...`

## Need Help?

- 📖 Check the updated [README.md](README.md)
- 🛠️ Read [DEVELOPMENT.md](DEVELOPMENT.md) for adding features
- 🐛 [Open an issue](https://github.com/YOUR_USERNAME/SIM7600g-H_Tutorial/issues)

## Summary

✅ **Renamed** package from `sms_logger` to `sim7600`  
✅ **Added** subcommand CLI structure  
✅ **Updated** all documentation  
✅ **Future-ready** for GPS and voice features  
✅ **Backwards compatible** (just change imports)

---

**Welcome to the new `sim7600` toolkit!** 🎉

