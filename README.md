# 🖥️ ServiceDesk — IT Service Request Portal

> A full-stack serverless IT support portal built entirely on AWS.  
> Submit tickets, track status, manage requests from an admin dashboard — with automated email notifications at every step.

![AWS](https://img.shields.io/badge/AWS-Lambda%20%7C%20DynamoDB%20%7C%20S3%20%7C%20SNS-FF6B6B?style=flat-square&logo=amazon-aws)
![Jenkins](https://img.shields.io/badge/CI%2FCD-Jenkins-D24939?style=flat-square&logo=jenkins)
![Python](https://img.shields.io/badge/Backend-Python%203.10-3776AB?style=flat-square&logo=python)
![Status](https://img.shields.io/badge/Status-Live-00C9A7?style=flat-square)

---

## ✨ Features

- **Submit Requests** — Name, email, location, description → saved to DynamoDB with unique ID
- **Track Requests** — Look up any request by its ID, see full details and current status
- **Admin Dashboard** — Protected login, live stats, full request table, inline status updates
- **SNS Email Notifications** — Users get email on submission and every time status changes
- **Real-time Home Stats** — Total, Pending, In Progress, Resolved — fetched live from DynamoDB
- **Jenkins CI/CD** — Push to GitHub → auto-deploys frontend to S3 + 4 Lambda functions
- **CloudFront CDN** — Fast global delivery of the static frontend

---

## 🏗️ Architecture

```
User/Admin Browser
      │
      ├──► CloudFront CDN ──► S3 (HTML / CSS / JS)
      │
      └──► API Gateway (us-east-2)
                │
                ├── POST /submit       ──► submitRequestFunction  ──► DynamoDB + SNS
                ├── GET  /track        ──► trackRequestFunction   ──► DynamoDB
                ├── GET  /list         ──► listRequestsFunction   ──► DynamoDB
                └── POST /update-status──► updateStatusFunction  ──► DynamoDB + SNS

GitHub Push ──► Jenkins Pipeline ──► S3 sync + Lambda deploy + CloudFront invalidation
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | HTML, CSS, JavaScript (Vanilla) |
| Hosting | AWS S3 + CloudFront |
| API | AWS API Gateway |
| Compute | AWS Lambda (Python 3.10) — 4 functions |
| Database | AWS DynamoDB |
| Email | AWS SNS (Simple Notification Service) |
| CI/CD | Jenkins Pipeline |
| Auth | SessionStorage-based admin login |

---

## 📁 Project Structure

```
service-request-portal/
├── frontend/
│   ├── index.html          # Home — real-time stats + recent requests
│   ├── submit.html         # Submit a new request
│   ├── track.html          # Track request by ID
│   ├── admin-login.html    # Admin login page
│   ├── admin.html          # Admin dashboard (auth protected)
│   ├── app.js              # Frontend API calls (submit + track)
│   └── style.css           # Global styles
├── backend/
│   ├── submit_request.py   # Save to DynamoDB + SNS email
│   ├── track_request.py    # Fetch single request by ID
│   ├── list_requests.py    # Scan all requests (admin)
│   └── update_status.py    # Update status + SNS notify user
├── Jenkinsfile             # CI/CD pipeline (9 stages)
└── Dockerfile              # Agent container (awscli + boto3)
```

---

## 🔌 API Endpoints

| Method | Route | Function | Description |
|---|---|---|---|
| POST | `/submit` | `submitRequestFunction` | Save request + send confirmation email |
| GET | `/track?id=XX` | `trackRequestFunction` | Fetch single request by ID |
| GET | `/list` | `listRequestsFunction` | Fetch all requests for admin |
| POST | `/update-status` | `updateStatusFunction` | Update status + notify user |

---

## 📧 SNS Email Flow

### On Submission
1. User submits form
2. Lambda saves to DynamoDB
3. Checks if email is a confirmed SNS subscriber
4. If confirmed → publishes confirmation email with Request ID
5. If new → subscribes email (user gets AWS confirmation → confirmed on next submit)

### On Status Change
1. Admin clicks Save on a row
2. Lambda updates DynamoDB
3. Fetches user email from the saved record
4. Publishes status update email with different content per status:
   - ⏳ Pending — "Request is in queue"
   - 🔄 In Progress — "Team is actively working on it"
   - ✅ Resolved — "Your request has been resolved"

---

## 🚀 AWS Setup (One-Time)

### 1. DynamoDB
- Table name: `service_requests`
- Partition key: `request_id` (String)

### 2. Lambda Functions
Create 4 functions, attach an IAM role with:
- `dynamodb:PutItem, GetItem, UpdateItem, Scan` on `service_requests`
- `sns:Publish, sns:Subscribe, sns:ListSubscriptionsByTopic` on your SNS topic

### 3. API Gateway
- Single REST API, 4 routes (see table above)
- Enable CORS on all routes
- Deploy to `prod` stage

### 4. SNS Topic
- Type: Standard
- Name: `service-request-notifications`
- Add `SNS_TOPIC_ARN` env variable to `submitRequestFunction` and `updateStatusFunction`

### 5. S3 + CloudFront
- S3 bucket with static website hosting enabled
- CloudFront distribution pointing to S3

---

## ⚙️ Jenkins Pipeline Stages

1. Checkout
2. Deploy Frontend to S3
3. Package & Deploy Submit Lambda
4. Package & Deploy Track Lambda
5. Package & Deploy List Lambda
6. Package & Deploy Update Status Lambda
7. Invalidate CloudFront Cache

---

## 🔐 Admin Access

- URL: `/admin-login.html`
- Default: `admin` / `admin@123`
- Change credentials in `admin-login.html` before production
- Session stored in `sessionStorage` — clears on tab close

---

## 💡 Suggested Improvements

- Move admin auth to AWS Cognito
- Add pagination to `/list` for large datasets
- Add DynamoDB GSI on `status` for faster filtered queries
- Add request priority levels (Low / Medium / High / Critical)
- CloudWatch alarms on Lambda error rates
- File attachment support via S3 presigned URLs

---

## 👨‍💻 Built By

**Sagar Ibrahim**  
Cloud & DevOps Engineer
`AWS` · `Jenkins` · `Python` · `DynamoDB` · `SNS` · `CloudFront`
