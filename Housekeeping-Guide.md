# 🛠️ Housekeeping Guide

This guide outlines the **daily coding workflow** and **Git operations** for all developers at Cybercore Solutions. Following this process ensures a smooth and efficient development cycle.

---

## 🔹 Branching Strategy

We follow a structured **branching strategy** to keep development organized:

- The **main branch** (`main`) contains stable, production-ready code.
- The **development branch** (`dev`), we dont use it just yet, stay in tune. 
- All new features and fixes should be worked on in a **new branch** created in this format. 
```bash
<issue-type>/<scope><#issue-number>-<feature-name>
```

### **Example Feature Branch**
Suppose you are working on a **backend feature** to implement user login verification, and the issue number is `#21`.

Your branch name should be:
```bash
feature/backend#21-Verify-Login
```
### Most of our task is feature, unless it is bug.

# 🛠 Git Workflow Guide

This guide explains how to properly create a new branch, commit changes, update it with the latest `main` branch, and submit a **Pull Request (PR)** for review.

---

## 🚀 Step 1: Start a New Feature Branch  
1. **Go to GitHub** and navigate to your repository.
2. **Find the feature you are starting** (Issue or Task).
3. Under the **"Development"** section, click **"Create a Branch"**.
![image](https://github.com/user-attachments/assets/f2b3d763-6f83-4e9f-a928-ecbf96a3af63)

4. Name your branch in the correct format:
**Example:**
```bash
feature/backend#21-Verify-Login
```
💡 Replace `feature/backend#21-Verify-Login` with the actual feature name and issue number.

5. Select Destination Repo and Branch Source
Branch Source: `main`
Destination Repo: The work repo (Backend/Frontend/Bot)
![image](https://github.com/user-attachments/assets/f20eae66-c131-4c91-827a-8c3f1e2d89cb)

6. Clone the repository and switch to your new branch:
```bash
git clone <repo-url>
cd <repo-folder>
git checkout feature/backend#21-Verify-Login
```

## 🔨 Step 2: Work on Your Feature
```bash
git commit -m "Updated _verify function"
git push origin feature/backend#21-Verify-Login
```
💡 Always commit with a meaningful message.

## 🔄 Step 3: Update Your Branch with the Latest main
Before finishing your work, *update your branch* with the latest main changes to prevent merge conflicts.

1. **Switch to `main` and pull the latest changes:**
```bash
git checkout main
git pull origin main
```

2. **Switch back to your feature branch:**
```bash
git checkout feature/backend#21-Verify-Login
```

3. **Merge `main` into your branch to update it:**
```bash
git merge main
```
💡 If there are conflicts, resolve them in your editor, then add and commit the resolved files.

4. **Push the updated branch to GitHub:**
```bash
git push origin feature/backend#21-Verify-Login
```

## 🔄 Step 4: Create a Pull Request (PR)
1. Go to **GitHub** and navigate to your repository (Frontend, Backend, Bot).
2. Click **New Pull Request**.
3. Select your **feature branch** as the source and `main` as the target.
4. Add a **clear title** and a **summary of the changes**.
5. **Assign your supervisor** for review:
   - **Backend PRs → Assign Ian**
   - **Frontend PRs → Assign Che**
6. **Notify Hong** if your PR is taking too long or blocking your work.

## 💡 Step 5: Document Completed Issues
Every time you complete an issue, document it in the corresponding location:
- **Backend Issues:** [Backend Documentation](https://github.com/Cybercore-Solutions/.github-private/wiki/Documentation:-Backend)
- **Frontend Issues:** [Frontend Documentation](https://github.com/Cybercore-Solutions/.github-private/wiki/Documentation:-Frontend-(Mini%E2%80%90app))
- **Bot Issues:** [Bot Documentation](https://github.com/Cybercore-Solutions/.github-private/wiki/Documentation:-Bot)

---

## 💬 Stay Engaged 

If you need any modifications or have any idea, start a discussion here [Discussion: Ideas](https://github.com/orgs/Cybercore-Solutions/discussions/categories/ideas)! 😊🚀

Your feedback helps us improve, so don’t hesitate to share your thoughts. Happy coding! 💻🎉  