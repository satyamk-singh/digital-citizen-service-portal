# GitHub Setup Instructions

Follow these steps after creating a new empty repository on GitHub.

## 1. Create GitHub Repository
1. Go to GitHub.
2. Click **New repository**.
3. Repository name suggestion: `digital-citizen-service-portal`.
4. Keep the repository empty at first. Do not add a README from GitHub because this project already includes one.

## 2. Initialize Git
Open a terminal inside the `digital-citizen-service-portal` folder and run:

```bash
git init
```

## 3. Add Files
```bash
git add .
```

## 4. Commit
```bash
git commit -m "Add week 1 e-governance project plan and prototype"
```

## 5. Add Remote
Replace `YOUR_GITHUB_USERNAME` with your actual GitHub username.

```bash
git remote add origin https://github.com/YOUR_GITHUB_USERNAME/digital-citizen-service-portal.git
```

## 6. Push to GitHub
```bash
git branch -M main
git push -u origin main
```

After pushing, copy the repository URL from GitHub and submit it in the internship portal.

## Important Note
Do not submit a fake GitHub URL. Use the real repository URL only after you create the repository and push this project.
