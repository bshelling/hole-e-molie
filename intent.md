# HoleeMoly: NOLA Pothole Reporting & Tracking Agent

## Problem Statement

Residents of New Orleans can report a pothole to NOLA-311, but the loop never closes for them. Once a request is filed there is no notification when it is resolved — you have to keep the reference number, remember to go back to the status page, or call 3-1-1 and ask. There is also no way for a resident to know whether someone has already reported the same pothole. Duplicate requests are closed by DPW rather than adding weight to the original, so the second reporter gets a notice that their request was a duplicate and nothing else.

The practical result is that people file once, hear nothing, assume nothing happened, and stop filing. The city loses the signal and the resident loses confidence that reporting is worth the effort.

## Solution

Build an AI agent using Strands SDK that:
- Accepts pothole reports via natural language chat
- Submits reports to NOLA-311's QuickBase system
- Periodically checks status of open reports
- Notifies residents when their reports are resolved via email, SMS, or in-app
- Detects duplicate reports to prevent redundant submissions and links users to existing reports

## Architecture

### Target System
```
┌─────────────────────────────────────────┐
│    Next.js Frontend (Port 3000)         │
│    - Chat UI for pothole reporting      │
│    - Status dashboard                   │
│    - Notification display               │
└──────────────┬──────────────────────────┘
               │ HTTP/WebSocket
               ▼
┌─────────────────────────────────────────┐
│    FastAPI Backend (Port 8000)          │
│    - /api/chat (WebSocket)              │
│    - /api/reports                       │
│    - /api/status                        │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│    Strands Agent (Conversation Handler) │
│    - report_pothole() tool              │
│    - check_status() tool                │
│    - search_nearby() tool               │
│    - manage_notifications() tool        │
└──────┬──────────────────┬───────────────┘
       │                  │
       ▼                  ▼
┌──────────────┐    ┌─────────────────┐
│ NOLA-311     │    │ DynamoDB        │
│ Connector    │    │ Data Layer      │
│ (Playwright) │    │ - Reports       │
└──────────────┘    │ - Users         │
                    │ - Status History│
                    └─────────────────┘
       │                  │
       ▼                  ▼
┌──────────────┐    ┌─────────────────┐
│ Notification │    │ AWS Lambda      │
│ Dispatcher   │    │ Status Poller   │
│ (SES/SNS)    │    │ (EventBridge)   │
└──────────────┘    └─────────────────┘
```

### Technology Stack

**Frontend:**
- Next.js 16.3.4 with React 19 and TypeScript
- Tailwind CSS 4 for styling
- Bun as package manager
- WebSocket for real-time chat

**Backend:**
- FastAPI for REST/WebSocket API
- Python 3.13 with uv package manager
- Strands SDK for agent conversation handling
- AWS Bedrock (Claude Sonnet 4.6) for LLM

**Data & Services:**
- AWS DynamoDB for data storage (with dynamodb-local for development)
- AWS SES for email notifications
- AWS SNS for SMS notifications
- AWS Lambda + EventBridge for background polling
- Playwright for NOLA-311 web automation

**Development:**
- DynamoDB Local for local testing
- NoSQLWorkbench for DynamoDB visualization

## Implementation Phases

### Phase 1: FastAPI Backend Foundation (Week 1, Days 1-3)
Set up FastAPI server with basic chat endpoint and project structure.

### Phase 2: NOLA-311 Integration (Week 1-2, Days 4-10)
Automate pothole report submission and status checking via Playwright browser automation.

### Phase 3: DynamoDB Data Layer (Week 2, Days 11-15)
Set up data storage with duplicate detection using geospatial indexing.

### Phase 4: Strands Agent Tools & Conversation Logic (Week 3, Days 16-22)
Build conversational agent with reporting and status checking capabilities.

### Phase 5: Next.js Chat Interface (Week 3-4, Days 23-28)
Build chat UI for pothole reporting connected to FastAPI backend.

### Phase 6: Notification System (Week 4-5, Days 29-33)
Multi-channel notifications (email, SMS, in-app) for status updates.

### Phase 7: Background Status Polling (Week 5, Days 34-36)
Automated periodic status checks via Lambda triggered by EventBridge.

### Phase 8: MVP Polish & Deployment (Week 6, Days 37-40)
Production-ready MVP with error handling, monitoring, and deployment.

## Key Features

### 1. Natural Language Pothole Reporting
Users describe potholes conversationally. The agent extracts:
- Location (address or landmark)
- Description of the pothole
- Severity indicators

### 2. Duplicate Detection
Before submitting, the system:
- Geocodes the address to coordinates
- Generates geohash (6 chars = ~1.2km × 0.6km grid)
- Queries nearby reports within 100 meters
- Offers to link user to existing report if duplicate found

### 3. NOLA-311 Integration
- Submits reports via automated QuickBase form interaction
- Extracts NOLA-311 reference number
- Periodically checks status by scraping status pages
- Handles form changes and CAPTCHA with fallbacks

### 4. Status Tracking & Notifications
- Stores reports in DynamoDB with status history
- Lambda polls NOLA-311 every 6 hours for active reports
- Sends notifications on status changes:
  - Email via AWS SES (primary)
  - SMS via AWS SNS (opt-in)
  - In-app (stored in DynamoDB)

### 5. User Dashboard
- View all submitted reports
- Check current status
- Update notification preferences
- See resolution history

## Data Model

### DynamoDB Single-Table Design

**Table:** `holeemoly-data`

**Entities:**
- `USER#<user_id> / PROFILE` - User contact info and preferences
- `REPORT#<report_id> / METADATA` - Report details and status
- `REPORT#<report_id> / STATUS#<timestamp>` - Status change history
- `LOCATION#<geohash_6> / REPORT#<report_id>` - Spatial index for duplicates
- `USER#<user_id> / REPORT#<timestamp>` - User's reports index

**Global Secondary Indexes:**
- **StatusIndex** (PK: status, SK: last_checked) - Find active reports for polling
- **LocationIndex** (PK: geohash_6, SK: created_at) - Spatial queries

## Development Workflow

1. **Local Development:**
   - Run dynamodb-local for database
   - Use NoSQLWorkbench to inspect data
   - FastAPI backend on port 8000
   - Next.js frontend on port 3000

2. **Testing:**
   - Each phase tested locally before PR
   - Unit tests for data layer and integrations
   - End-to-end tests for conversation flows

3. **Deployment:**
   - Backend: AWS Lambda or EC2
   - Frontend: Vercel
   - Database: AWS DynamoDB
   - Background jobs: Lambda + EventBridge

## Success Metrics

- Number of reports filed through agent
- Duplicate detection accuracy (false positive/negative rate)
- Time from report to resolution notification
- User retention (repeat usage)
- NOLA-311 integration uptime (target: 95%+)
- Notification delivery rate (target: 98%+)
- Background polling success rate (target: 95%+)

## Cost Estimation

**Development (local):** $0/month (dynamodb-local, free tier AWS services)

**Production (100 reports/month):**
- DynamoDB: $1.50
- Lambda: $0.50
- SES: $0.03
- SNS: $1.00 (SMS opt-in only)
- CloudWatch: $2.00
- Bedrock: $15.00
- **Total: ~$20/month**

**Production scale (1000 reports/month):** ~$80/month

## References

- NOLA-311 Service Request Form: https://opcd.quickbase.com/nav/app/bn79jh4a4/table/bn8jze2s7/action/nwr?nexturl=%2Fdb%2Fbn79jh4a4%3Fa%3Dshowpage%26pageIdV2%3Dquickbase.com-DashboardGroup-9e8df6e8-4d3f-4dc9-918f-ce43c863dfda&page=3
- Strands SDK: https://docs.strands.ai/
- DynamoDB Local: https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DynamoDBLocal.html
