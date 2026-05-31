# camKapture Quick Start Guide

Get up and running with camKapture in 5 minutes!

## 📦 Installation

### Step 1: Clone and Navigate
```bash
git clone https://github.com/manojuppala/camKapture.git
cd camKapture
```

### Step 2: Create Virtual Environment
```bash
# On macOS/Linux
python3 -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Run the Application
```bash
python main.py
```

That's it! The GUI should open with your camera preview.

---

## 🎮 Basic Usage

### Taking Photos
1. Click **"📷 Capture Photo"** button
2. Photo is saved to `~/Pictures/camKapture/`
3. A flash effect confirms capture

### Recording Videos
1. Click **"▶ Start Recording"**
2. Recording indicator shows in status bar
3. Click **"⏹ Stop Recording"** when done
4. Video is saved to `~/Videos/camKapture/`

### Applying Effects
1. Select effect from dropdown (e.g., "Grayscale", "Cartoonify")
2. Adjust parameters if available (sliders appear below)
3. Click **"Apply"** to see the effect in preview
4. Click **"Clear"** to remove effect
5. Capture photos/videos with effect applied

### Popular Effects to Try
- **Sepia** - Classic vintage brown tone
- **Cartoonify** - Cartoon-style rendering
- **Edge Detection** - See edges in your video
- **Vintage** - Old photo effect
- **Blur** - Smooth background blur

---

## ⚙️ Configuration

### Change Resolution
1. Menu → **Settings** → **Preferences**
2. Click preset buttons: **720p**, **1080p**, or **4K**
3. Or enter custom width/height
4. Click **Save** and restart

### Change Output Folders
1. Menu → **Settings** → **Preferences**
2. Go to **Output** tab
3. Click **Browse** next to Image/Video directory
4. Select folder and click **Save**

### Adjust Frame Rate
1. Menu → **Settings** → **Preferences**
2. Change FPS value (15-60)
3. Click **Save** and restart

---

## 🎨 Effect Examples

### Brightness Adjustment
1. Select "Brightness" from dropdown
2. Adjust slider (-100 to +100)
3. Click "Apply"
4. Great for low-light situations!

### Artistic Cartoonify
1. Select "Cartoonify"
2. Click "Apply"
3. Creates comic-book style video
4. Perfect for fun selfies!

### Professional HDR
1. Select "HDR"
2. Click "Apply"
3. Enhances details and colors
4. Great for product demos!

---

## 📁 File Locations

### Your Captures
- **Images**: `~/Pictures/camKapture/`
- **Videos**: `~/Videos/camKapture/`

### Configuration & Logs
- **Config**: `~/.camkapture/config.json`
- **Logs**: `~/.camkapture/logs/`

---

## 🆘 Troubleshooting

### Camera Not Detected
- Ensure camera is connected
- Check camera permissions in OS settings
- Try different camera device ID in settings

### Application Won't Start
```bash
# Check Python version (needs 3.7+)
python --version

# Reinstall dependencies
pip install --force-reinstall -r requirements.txt
```

### Effects Not Working
- Some effects require specific OpenCV builds
- Try different effect if one fails
- Check logs at `~/.camkapture/logs/`

### Performance Issues
- Lower resolution in settings (try 720p)
- Reduce FPS to 30 or lower
- Avoid CPU-intensive effects on slower machines

---

## 💡 Pro Tips

1. **Keyboard Shortcut**: Just close the window to exit
2. **Quick Access**: Create desktop shortcut to `main.py`
3. **Custom Presets**: Edit `~/.camkapture/config.json` directly
4. **Multiple Effects**: Apply one, capture, then apply another
5. **Best Quality**: Use 1080p @ 30 FPS for balanced quality/performance

---

## 📚 Learn More

- Full documentation: See [README.md](README.md)
- Add new effects: See [CONTRIBUTING.md](CONTRIBUTING.md)
- Report issues: GitHub Issues

---

**Enjoy creating with camKapture! 📸✨**
