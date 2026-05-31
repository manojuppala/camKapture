# camKapture Effects Guide

Complete reference for all 40+ image effects available in camKapture.

## Quick Reference

| Effect | Category | Best For | Intensity |
|--------|----------|----------|-----------|
| Grayscale | Basic | B&W photos | N/A |
| Sepia | Basic | Vintage look | Medium |
| Cartoonify | Artistic | Fun selfies | High |
| Sketch | Artistic | Artistic photos | High |
| Vintage | Artistic | Retro style | Medium |
| HDR | Artistic | Enhanced details | Medium |
| Edge Detection | Edge | Line art | High |
| Blur | Adjustment | Background blur | Low-Med |
| Sharpen | Adjustment | Crisp details | Low |
| Color Pop | Color | Highlight colors | High |

## Effect Details

### Basic Effects

#### Grayscale
- **Description**: Converts image to black and white
- **Use Case**: Classic B&W photography
- **Parameters**: None
- **Performance**: Fast

#### Sepia
- **Description**: Warm brown-tone vintage effect
- **Use Case**: Old photograph look
- **Parameters**: Intensity (0.0-1.0)
- **Performance**: Fast

#### Black & White
- **Description**: High-contrast threshold-based B&W
- **Use Case**: Dramatic contrast photos
- **Parameters**: Threshold (0-255)
- **Performance**: Fast

#### Posterize
- **Description**: Reduces number of colors
- **Use Case**: Pop-art, graphic design look
- **Parameters**: Levels (2-16)
- **Performance**: Medium

#### Solarize
- **Description**: Partial color inversion
- **Use Case**: Psychedelic effects
- **Parameters**: Threshold (0-255)
- **Performance**: Fast

---

### Artistic Effects

#### Cartoonify
- **Description**: Comic book / cartoon style with edge detection
- **Use Case**: Fun selfies, creative videos
- **Parameters**: Bilateral filter strength, edge thresholds
- **Performance**: Medium
- **Tips**: Works best with good lighting

#### Sketch
- **Description**: Pencil sketch effect
- **Use Case**: Artistic rendering
- **Parameters**: Colored (bool)
- **Performance**: Medium

#### Warm Glow
- **Description**: Soft warm tone with gaussian glow
- **Use Case**: Romantic/cozy atmosphere
- **Parameters**: Intensity (0.0-1.0)
- **Performance**: Medium

#### Cool Tone
- **Description**: Cyan/blue cool tone
- **Use Case**: Professional, modern look
- **Parameters**: Intensity (0.0-1.0)
- **Performance**: Fast

#### Film Grain
- **Description**: Adds analog film grain noise
- **Use Case**: Film photography simulation
- **Parameters**: Intensity (0.0-1.0)
- **Performance**: Fast
- **Tips**: Use low intensity (0.05-0.15) for subtle effect

#### Cross Process
- **Description**: Cross-processed film look (high contrast, shifted colors)
- **Use Case**: Retro/hipster photography
- **Parameters**: None
- **Performance**: Fast

#### Infrared
- **Description**: Simulates infrared photography
- **Use Case**: Surreal, artistic photos
- **Parameters**: None
- **Performance**: Fast

#### Bleach Bypass
- **Description**: Desaturated, high-contrast film technique
- **Use Case**: Gritty, cinematic look
- **Parameters**: Intensity (0.0-1.0)
- **Performance**: Medium

#### Mirror
- **Description**: Kaleidoscope/mirror symmetry
- **Use Case**: Abstract art
- **Parameters**: Mode (horizontal/vertical/quad)
- **Performance**: Fast

---

### Adjustments

#### Denoise
- **Description**: Advanced noise reduction
- **Use Case**: Low-light video cleanup
- **Parameters**: Strength (1-30)
- **Performance**: Slow
- **Tips**: Strength 10-15 recommended, computationally intensive

#### Motion Blur
- **Description**: Directional blur for motion effect
- **Use Case**: Speed/motion emphasis
- **Parameters**: Kernel size, angle
- **Performance**: Medium

#### Auto Level
- **Description**: Automatic histogram normalization
- **Use Case**: Quick color/brightness correction
- **Parameters**: None
- **Performance**: Fast

#### Gamma
- **Description**: Gamma curve adjustment
- **Use Case**: Brightness correction without clipping
- **Parameters**: Gamma (0.1-3.0)
- **Performance**: Fast

---

### Color Effects

#### Color Pop
- **Description**: Keeps one color vibrant, desaturates rest
- **Use Case**: Highlight specific objects (e.g., red dress in B&W scene)
- **Parameters**: Hue target (0-179), range (10-50)
- **Performance**: Fast
- **Tips**: 
  - Red: 0
  - Green: 60
  - Blue: 120

#### Duo Tone
- **Description**: Maps grayscale to two-color gradient
- **Use Case**: Stylized portraits, graphic design
- **Parameters**: Color1, Color2 (RGB tuples)
- **Performance**: Fast

#### LUT (Look-Up Table)
- **Description**: Professional color grading presets
- **Use Case**: Cinematic color grading
- **Parameters**: Type (warm/cool/contrast)
- **Performance**: Very Fast

#### Color Balance
- **Description**: Adjust individual RGB channels
- **Use Case**: Color correction, creative toning
- **Parameters**: Red, Green, Blue multipliers
- **Performance**: Fast

---

## Performance Guide

### Fast Effects (Real-time even on 4K)
- Grayscale, Sepia, Invert, Flip
- Brightness, Contrast
- Color Balance, Channel Swap
- Posterize, Solarize

### Medium Effects (Smooth on 1080p)
- Cartoonify, Sketch
- Most artistic effects
- Blur, Sharpen, Emboss
- Motion Blur

### Intensive Effects (Best at 720p)
- Denoise (very slow)
- Oil Painting (if available)
- Heavy blur with large kernels

## Effect Combinations

Try these combinations for unique looks:

1. **Film Look**: Vintage + Film Grain + Vignette
2. **Dramatic**: Black & White + Auto Level + Sharpen
3. **Retro**: Cross Process + Warm Glow
4. **Artistic**: Sketch + Sepia
5. **Cinematic**: Bleach Bypass + LUT (contrast)
6. **Pop Art**: Posterize + Color Balance

## Tips & Tricks

- **For Selfies**: Warm Glow, HDR, Auto Level
- **For Landscapes**: HDR, Sharpen, Contrast
- **For B&W**: Black & White, Auto Level, Sharpen
- **For Fun**: Cartoonify, Mirror, Color Pop, Pixelate
- **For Atmosphere**: Vintage, Film Grain, Vignette
