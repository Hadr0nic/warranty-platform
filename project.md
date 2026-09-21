### 1. Use of Design Pattern

- The system must be designed using appropriate design patterns.

### 2. User Authentication via Token + Email or SMS (using sms.ir panel)

- Users should be able to log in via token + email or SMS.
    
- Password recovery and account verification must be available:
    
    - For SMS: send an activation code.
        
    - For email: send a secure activation link with expiration date.
        
- Security of links and tokens must be fully reviewed and implemented.
    

### 3. Bulk Email Sending by Admin

- Admin should be able to send formatted emails via an HTML editor to all users or specific groups.
    
- The system must support extensible and secure templates.
    

### 4. File and Image Management with Arvan Cloud

- [ ] All images and files must be stored, edited, deleted, and downloaded via Arvan Cloud (two‑way integration).
    
- [ ] Error handling, access control, and temporary download links are mandatory.
    
- [x] 5. Comment Notification
    
- [ ] As soon as a new comment is registered, a personalized email should be sent to all admins.
    
- [ ] The email text must use the system’s template engine.
    

### 6. Create Test Users via Command Line

- [ ] Admin should be able to run a management command to create 10 test users with meaningful data.
    
- [x] 7. Project Structure Integration
    
- [ ] All templates must be fully integrated.
    
- [ ] All models must have unique and standard slugs. (Research slug functionality.)
    
- [ ] 8. Internal Password Manager
    
- [ ] The system should:
    
    - [ ] Receive a secondary password from the user.
        
    - [ ] Store it securely in the database.
        
    - [ ] Before storage, check the password using `django-pwned-passwords` to ensure it is not in leaked password lists.
        
    - [ ] Explain how hashing and security management of this password is handled.
        
- [ ] 9. Database Location Considerations
    
- [ ] Pay attention to database allocation in terms of security, accessibility, and scalability.
    
- [ ] Explain the reason for your choice.
    
- [ ] 10. Full Localization of Admin Panel
    
- [ ] Names of all apps, models, and fields in the admin panel must be displayed in Persian.
    
- [ ] All models must have:
    
    - [ ] Creation date
        
    - [ ] Last update date
        
    - [ ] Displayed in the Jalali (Shamsi) calendar format.
        
- [ ] 11. Export Users
    
- [ ] Ability to export user tables in **Excel and PDF** with proper Persian encoding and fonts.
    
- [ ] 12. Advanced Admin List View Features
    
- [ ] For users in the admin panel:
    
    - [ ] Practical filters
        
    - [ ] Smart search fields (based on your defined project)
        
    - [ ] Filter by “having or not having comments”
        
    - [ ] Inline editing directly in the list
        
    - [ ] Inline display and management of comments.
        
- [ ] 13. Section Management
    
- [ ] Admin can create up to 7 different sections.
    
- [ ] Sections order can be changed via drag & drop in the admin panel.
    
- [ ] Sections must support a tree structure up to 3 levels (e.g., Section → 1.1 → 1.1.1).
    
- [ ] 14. Rate Limiting with Middleware
    
- [ ] Using appropriate middleware:
    
    - [ ] If a user sends more than 30 requests within 5 minutes, they should be automatically blocked.
- [ ] 15. Comprehensive Logging System
    
- [ ] A standard, extensible logging system must be designed for the entire project (apps, services, repositories, models, etc.).
    
- [ ] Log levels (INFO, WARNING, ERROR, CRITICAL) must be respected.
    
- [ ] 16. Email Sending with Celery
    
- [ ] All email sending must be handled via Celery tasks.
    
- [ ] Retry and failure management is mandatory.
    
- [ ] 17. Restricted Admin Panel (Admin Level 0)
    
- [ ] Define a dedicated URL for Admin Level 0 (Messenger Admin).
    
- [ ] This admin can only:
    
    - [ ] Log in to the panel
        
    - [ ] Send a message to higher‑level admins
        
- [ ] They must have no access to reports, logs, or model change history.
    
- [ ] 18. Project Settings Management
    
- [ ] `.env` and `requirements.txt` files must be properly created.
    
- [ ] Sensitive settings must only be managed via environment variables.
    
- [ ] 19. Git Commit Standards
    
- [ ] All changes must be committed in Git using the following format:
    
    Code
    
    ```
    <app/feature>(<branch>): <add|fix|delete> description
    ```
    
- [ ] 20. Automatic Daily Email
    
- [ ] Every day at 18:00 Khartoum time, an automatic email with the message “Good evening” must be sent to users.
    
- [ ] This should be implemented using the Notification System + Django Signals.
    
- [ ] 21. Image Minification in Admin
    
- [ ] When uploading an image in the admin panel, the admin should be able to choose whether the image should be minified or not.
    
- [ ] Implementation must follow proper image minification concepts.
    
- [ ] 22. Login with Google Account
    
- [ ] Users should be able to register/login via Google OAuth.
    
- [ ] Explain how to manage linking the Google account to the internal account.
    

&nbsp;