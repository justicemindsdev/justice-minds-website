# Justice Minds Website - Deployment Guide to justice-minds.com

## ✅ Current Status

Your Guardian-style website is now on GitHub and ready to go live at **justice-minds.com**!

**Repository**: https://github.com/justicemindsdev/justice-minds-website
**CNAME File**: ✅ Created and pushed (commit 5cd65f5)

---

## 🚀 Step 1: Enable GitHub Pages (Do This Now)

1. Go to your repository: https://github.com/justicemindsdev/justice-minds-website
2. Click **Settings** (in the top menu)
3. Click **Pages** (in the left sidebar)
4. Under "Build and deployment":
   - **Source**: Select "Deploy from a branch"
   - **Branch**: Select "main" and "/ (root)"
   - Click **Save**

GitHub will automatically detect your CNAME file and configure the custom domain!

---

## 🌐 Step 2: Configure DNS Settings

You need to update your DNS records at your domain registrar (where you manage justice-minds.com).

### Option A: Using an Apex Domain (Recommended)

Add these **A Records**:

```
Type: A
Name: @
Value: 185.199.108.153

Type: A  
Name: @
Value: 185.199.109.153

Type: A
Name: @
Value: 185.199.110.153

Type: A
Name: @
Value: 185.199.111.153
```

### Option B: Using www subdomain (Alternative)

Add this **CNAME Record**:

```
Type: CNAME
Name: www
Value: justicemindsdev.github.io
```

---

## 🔒 Step 3: Enable HTTPS (After DNS Propagates)

1. Wait 10-60 minutes for DNS to propagate
2. Go back to **Settings → Pages**
3. Check the box: "Enforce HTTPS"
4. GitHub will automatically provision an SSL certificate

---

## ⏱️ Timeline

- **Immediate**: GitHub Pages builds your site (~2-5 minutes)
- **10-60 minutes**: DNS propagates worldwide
- **1-2 hours**: SSL certificate issued
- **Result**: justice-minds.com shows your new Guardian-style website!

---

## 🎨 What's Going Live

Your new website includes:

✅ Homepage with Guardian-style hero and article grid
✅ Investigation: The Silent Exploitation (Hilton investigation)
✅ Shubham's Story
✅ Shubham Sick Brother article
✅ Cultural Exploitation article
✅ Measuring Competence Beyond Exams
✅ The One Person Principle
✅ Institutional Investigation S188
✅ Cultural Conditioning & Freedom
✅ Ben Oversight Validation
✅ About page
✅ Privacy Policy
✅ Terms of Service
✅ All Guardian-style design elements
✅ Mobile-responsive navigation
✅ Audio evidence sections
✅ Court statistics dashboard

---

## 🔍 Verification

Once DNS propagates, verify your site is live:

```bash
# Check DNS propagation
dig justice-minds.com

# Test the website
curl -I https://justice-minds.com
```

Or simply visit: https://justice-minds.com in your browser!

---

## 🛠️ Troubleshooting

### Site not loading?
- Check DNS propagation: https://dnschecker.org (search for justice-minds.com)
- Ensure GitHub Pages is enabled in Settings → Pages
- Verify CNAME file exists in repository

### Certificate error?
- Wait 1-2 hours for SSL certificate to be issued
- Make sure "Enforce HTTPS" is checked in GitHub Pages settings

### Wrong domain showing?
- Verify CNAME file contains only: `justice-minds.com`
- Check custom domain in GitHub Pages settings matches

---

## 📞 Need Help?

If you encounter issues:
1. Check GitHub Pages deployment status in Settings → Pages
2. Review DNS settings at your registrar
3. Wait for full DNS propagation (can take up to 48 hours, usually much faster)

---

**Your new Guardian-style website is ready to replace the old justice-minds.com site!**
