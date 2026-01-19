# 🏴‍☠️ Bits of the Black Pearl - Pirates CTF Theme

> *"Only those who seek shall uncover the truth"*

A fully immersive **Pirates of the Caribbean**-themed CTFd platform that transforms your Capture The Flag competition into an epic pirate adventure on the high seas.

![Pirates Theme Banner](https://img.shields.io/badge/Theme-Pirates%20of%20the%20Caribbean-gold?style=for-the-badge)
![CTFd Compatible](https://img.shields.io/badge/CTFd-Compatible-blue?style=for-the-badge)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white)

---

![Platform](/image.png)

---

## ⚓ Overview

**Bits of the Black Pearl** is a custom CTFd theme that brings the mystique and adventure of Pirates of the Caribbean to your cybersecurity competitions. With cinematic video intros, animated backgrounds, golden text effects, and a complete pirate aesthetic, this theme creates an unforgettable experience for participants.

### ✨ Key Features

- 🎬 **Video Introduction**: Auto-playing cinematic intro with skip functionality
- 🌊 **Animated Background**: Dynamic lighting effects that simulate ocean waves
- 💎 **Golden Text Animation**: Smooth shimmer effects on the main title with rustic glow
- 🏴‍☠️ **Pirate Aesthetics**: Jolly Roger emblems, treasure-themed colors, and nautical typography
- 📱 **Fully Responsive**: Optimized for desktop, tablet, and mobile devices
- ⚡ **Session Memory**: Intro video plays once per session
- 🎨 **Custom Branding**: Dual-logo support for organizers and creators

---

## 🎯 Theme Highlights

### Visual Experience
- **Color Palette**: Rich golds (#d4af37, #b9a27d), deep reds (#a4161a), and weathered browns
- **Typography**: Bold, adventure-style fonts with glowing effects
- **Icons**: Pirate-themed elements (⚓ anchors, ⚔️ crossed swords, ☠️ skulls)
- **Animations**: Smooth fade-ins, shimmer effects, and minimal floating motion

### User Interface
- Clean, centered layout with optimal spacing
- Prominent call-to-action button with hover effects
- Developer credits section with elegant styling
- Warning banners and decorative separators

### Technical Features
- Session-based video playback control
- Progressive animation loading
- Optimized asset delivery
- Cross-browser compatibility

---

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose installed
- CTFd platform (compatible with CTFd 3.x)
- Basic knowledge of Docker deployment

### Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/pirates-ctf-theme.git
   cd pirates-ctf-theme
   ```

2. **Deploy with Docker Compose**
   ```bash
   docker-compose up -d
   ```

3. **Access Your Platform**
   - Navigate to `http://localhost:8000` (or your configured domain)
   - Watch the epic intro video
   - Begin your pirate adventure!

### File Structure
```
pirates-ctf-theme/
├── docker-compose.yml          # Docker deployment configuration
├── theme/                      # Theme assets directory
│   ├── templates/              # HTML templates
│   │   └── index.html         # Main landing page
│   ├── static/                # Static assets
│   │   ├── css/              # Stylesheets
│   │   ├── js/               # JavaScript files
│   │   └── img/              # Images and media
│   │       ├── pirates.png   # Main pirate emblem
│   │       ├── vid-3.mp4     # Intro video
│   │       ├── teknofest-logo.png
│   │       └── wlwj-logo.png
│   └── assets/               # Additional theme assets
└── README.md                  # This file
```

---

## 🎨 Customization

### Adding Your Logos
Replace the following files with your organization's logos:
- `theme/static/img/teknofest-logo.png` - Organizing entity logo
- `theme/static/img/wlwj-logo.png` - Creating team logo

**Recommended specs**: PNG format, transparent background, max width 200px

### Changing the Intro Video
Replace `theme/static/img/vid-3.mp4` with your custom video:
- **Format**: MP4 (H.264 codec recommended)
- **Resolution**: 1920x1080 or higher
- **Duration**: 30-60 seconds for best experience
- **Size**: Optimize for web (under 50MB recommended)

### Customizing Colors
Edit the CSS variables in the theme to match your brand:
```css
/* Main gold color */
#d4af37

/* Rustic brown/bronze */
#8b7355, #b9a27d

/* Accent red */
#a4161a

/* Light cream */
#f1efea
```

### Modifying Animations
Adjust animation speeds in the CSS:
- `goldenShimmer`: Change duration from `2.5s` to your preference
- `rusticGlow`: Modify glow intensity and timing
- `minimalFloat`: Adjust floating distance (currently 3px)

---

## 🛠️ Configuration

### Docker Compose Setup
The included `docker-compose.yml` is pre-configured for CTFd deployment. Key settings:

```yaml
services:
  ctfd:
    image: ctfd/ctfd:latest
    volumes:
      - ./theme:/opt/CTFd/CTFd/themes/pirates
    ports:
      - "8000:8000"
    environment:
      - SECRET_KEY=your_secret_key_here
      - DATABASE_URL=mysql+pymysql://ctfd:ctfd@db/ctfd
```

### Environment Variables
- `SECRET_KEY`: Generate a secure random key
- `DATABASE_URL`: Configure your database connection
- `REDIS_URL`: Optional, for caching and sessions

---

## 📸 Screenshots

### Landing Page
![Landing Page Preview](screenshot-landing.png)
*The main entry point with animated golden title and pirate emblem*

### Video Intro
![Video Intro](screenshot-intro.png)
*Cinematic intro video with skip button*

### Challenge Page
![Challenges](screenshot-challenges.png)
*Themed challenge interface maintaining the pirate aesthetic*

---

## 🎭 Theme Components

### HTML Templates
- **index.html**: Main landing page with video overlay
- **base.html**: Extended base template (inherited from CTFd)

### JavaScript Features
- Video autoplay with fallback handling
- Session storage for intro state
- Smooth fade transitions
- Error handling and recovery

### CSS Animations
- **fadeInUp**: Entry animations for content
- **fadeInDown**: Logo entrance effects
- **goldenShimmer**: Text shimmer effect
- **rusticGlow**: Pulsating glow animation
- **minimalFloat**: Subtle floating motion

---

## 🤝 Contributing

We welcome contributions to make this theme even better! Here's how you can help:

1. **Fork the Repository**
2. **Create a Feature Branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Commit Your Changes**
   ```bash
   git commit -m 'Add some amazing feature'
   ```
4. **Push to the Branch**
   ```bash
   git push origin feature/amazing-feature
   ```
5. **Open a Pull Request**

### Contribution Ideas
- Additional page templates
- Alternative color schemes
- Mobile UI improvements
- Performance optimizations
- Accessibility enhancements
- Internationalization support

---

## 🐛 Troubleshooting

### Video Not Playing
- **Issue**: Intro video doesn't autoplay
- **Solution**: Modern browsers block unmuted autoplay. The theme includes fallback to muted playback.

### Animation Performance
- **Issue**: Animations lag on mobile devices
- **Solution**: Reduce animation complexity in `style` section or disable for mobile viewports.

### Logo Display Issues
- **Issue**: Logos appear stretched or misaligned
- **Solution**: Ensure logos are properly sized (max 200px width) and use transparent backgrounds.

### Docker Deployment Fails
- **Issue**: Container won't start
- **Solution**: Check Docker logs with `docker-compose logs ctfd` and verify all paths in docker-compose.yml.

---

## 📜 License

This theme is released under the **MIT License**. See [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2024 WL&WJ

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction...
```

---

## 👥 Credits

### Development Team
- **[Aman Shahid](https://github.com/dev-sire)** - Lead Developer & Theme Designer
- **[Abdul Wasay Khan](https://github.com/AlWasay125)** - Co-Developer & Challenge Creator

### Special Thanks
- **TeknoFest** - For organizing the event
- **CTFd Team** - For the amazing platform
- **Pirates of the Caribbean** - For the inspiration

---

## 🔗 Links

- **CTFd Official**: [https://ctfd.io](https://ctfd.io)
- **Documentation**: [CTFd Docs](https://docs.ctfd.io)
- **Report Issues**: [GitHub Issues](https://github.com/yourusername/pirates-ctf-theme/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/pirates-ctf-theme/discussions)

---

## 📞 Contact

For questions, suggestions, or support:

- **Email**: your-email@example.com
- **Discord**: YourDiscord#0000
- **Twitter**: [@yourhandle](https://twitter.com/yourhandle)

---

<div align="center">

### ⚓ Set Sail on Your CTF Adventure! ⚓

*Made with* 💎 *by the WL&WJ crew*

[![GitHub Stars](https://img.shields.io/github/stars/yourusername/pirates-ctf-theme?style=social)](https://github.com/yourusername/pirates-ctf-theme)
[![GitHub Forks](https://img.shields.io/github/forks/yourusername/pirates-ctf-theme?style=social)](https://github.com/yourusername/pirates-ctf-theme)

</div>