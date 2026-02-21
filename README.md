# Kairos-Voice
### Auditory Inspection Module

> **"Making the invisible audible via**
> **mathematical rigor."**

**Kairos-Voice** is a tactical forensic 
tool by **Gobode Labs**. It converts 
raw text into sanitized speech for 
hands-free system auditing.

---

## 🛡️ Self-Defense Logic

* **Input Sanitization**
  Regex layers strip unsafe symbols 
  to prevent engine injection.

* **Threaded Resilience**
  Separated UI/Audio threads keep 
  the interface responsive.

* **WSL2 Compatibility**
  Built for the WSLg PulseServer 
  and `espeak` kernel.



---

## 🚀 Installation

### 1. System Requirements
* Linux or WSL2 (WSLg)
* `espeak-ng`
* `libpulse0`

### 2. Deployment
```bash
# Clone and enter
git clone 
cd kairos-voice

# Environment setup
python3 -m venv venv
source venv/bin/activate
pip install pyttsx3
