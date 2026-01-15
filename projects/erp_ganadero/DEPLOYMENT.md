# Deployment Guide - ERP Ganadero V2

## 🚀 Quick Deploy to Vercel

### Prerequisites
- GitHub account
- Vercel account (free tier: https://vercel.com/signup)
- Code pushed to GitHub

---

## 📋 Step-by-Step Deployment

### Option A: Vercel Dashboard (Easiest) ⭐

1. **Go to Vercel**
   - Visit https://vercel.com
   - Sign in with GitHub

2. **Import Project**
   - Click "Add New..." → "Project"
   - Select your GitHub repository: `ANTIGRAVITY`
   - Click "Import"

3. **Configure Project**
   - **Framework Preset**: Vite
   - **Root Directory**: `projects/erp_ganadero/frontend-v2`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
   - **Install Command**: `npm install`

4. **Environment Variables** (Optional)
   ```
   VITE_API_URL=http://127.0.0.1:8000
   VITE_APP_ENV=production
   ```

5. **Deploy**
   - Click "Deploy"
   - Wait 2-3 minutes
   - Get your production URL: `https://your-project.vercel.app`

---

### Option B: Vercel CLI (Advanced)

1. **Install Vercel CLI**
   ```bash
   npm i -g vercel
   ```

2. **Login**
   ```bash
   vercel login
   ```

3. **Deploy**
   ```bash
   cd /Users/franciscocambero/Anitgravity/projects/erp_ganadero/frontend-v2
   vercel --prod
   ```

4. **Follow Prompts**
   - Set up and deploy: Y
   - Which scope: [your account]
   - Link to existing project: N
   - Project name: erp-ganadero-v2
   - Directory: ./
   - Override settings: N

---

## ✅ Post-Deployment Checklist

### 1. Verify HTTPS
- [ ] Visit your Vercel URL
- [ ] Confirm HTTPS (🔒 in browser)
- [ ] No SSL warnings

### 2. Test PWA Installation
- [ ] Open on mobile browser
- [ ] See install prompt
- [ ] Install to home screen
- [ ] Launch from home screen

### 3. Test Service Worker
- [ ] Open DevTools → Application → Service Workers
- [ ] Verify service worker is active
- [ ] Test offline mode (DevTools → Network → Offline)

### 4. Test Functionality
- [ ] Navigate all pages
- [ ] Test bottom navigation
- [ ] Test forms
- [ ] Test data entry

---

## 🌐 Custom Domain (Optional)

### Add Custom Domain

1. **In Vercel Dashboard**
   - Go to Project Settings → Domains
   - Click "Add"
   - Enter your domain: `erpganadero.com`

2. **Configure DNS**
   - Add CNAME record:
     ```
     Type: CNAME
     Name: www (or @)
     Value: cname.vercel-dns.com
     ```

3. **Verify**
   - Wait for DNS propagation (5-60 minutes)
   - Vercel will auto-issue SSL certificate

---

## 📊 Monitoring & Analytics

### Vercel Analytics (Built-in)
- Automatic performance monitoring
- Real user metrics
- Core Web Vitals

### Enable Analytics
1. Go to Project Settings → Analytics
2. Enable Vercel Analytics
3. View metrics in dashboard

---

## 🔧 Troubleshooting

### Build Fails
**Problem**: Build command fails  
**Solution**:
```bash
# Test build locally first
cd frontend-v2
npm run build

# Check for errors
# Fix any TypeScript/build errors
```

### Service Worker Not Working
**Problem**: PWA not installable  
**Solution**:
- Verify HTTPS is enabled
- Check `vercel.json` headers
- Clear browser cache
- Test in incognito mode

### 404 on Refresh
**Problem**: Page not found when refreshing  
**Solution**:
- Verify `vercel.json` rewrites configuration
- Should redirect all routes to `/index.html`

---

## 🎯 Production URLs

After deployment, you'll get:
- **Production**: `https://erp-ganadero-v2.vercel.app`
- **Preview**: `https://erp-ganadero-v2-git-[branch].vercel.app`

---

## 📱 Share with Beta Users

### Installation Instructions for Users

**iOS (Safari)**:
1. Open https://your-app.vercel.app
2. Tap Share button (⬆️)
3. Scroll down, tap "Add to Home Screen"
4. Tap "Add"

**Android (Chrome)**:
1. Open https://your-app.vercel.app
2. Tap menu (⋮)
3. Tap "Install app" or "Add to Home screen"
4. Tap "Install"

---

## 🚀 Next Steps

1. ✅ Deploy to Vercel
2. ✅ Test on real devices
3. ✅ Share URL with 3-5 beta users
4. ✅ Collect feedback
5. ✅ Iterate based on user input

---

**Deployment Platform**: Vercel  
**Estimated Time**: 10-15 minutes  
**Cost**: Free (Hobby tier)
