# NP Operator — Usage Scenarios
# سيناريوهات استخدام — مشغل الإشعارات

## Role Overview

- **Title**: Notification Operator / مشغل الإشعارات
- **CAPS Capabilities**: NP_send_notifications, NP_view_logs, NP_manage_preferences
- **Primary DocTypes**: NP Notification Log, NP Queue, NP User Preference
- **Device**: Desktop / Tablet

## Daily Scenarios (يومي)

### DS-001: Send Ad-Hoc Notification
- **Goal**: Send a one-off notification to specific recipients
- **Steps**:
  1. Use API or quick-send form
  2. Select channel, template, and recipients
  3. Submit notification
  4. Verify delivery in NP Notification Log

### DS-002: Clear Notification Queue
- **Goal**: Process stuck items in the queue
- **Steps**:
  1. Navigate to NP Core → NP Queue
  2. Filter by status = "Pending" with old creation dates
  3. Retry or cancel stuck items
  4. Verify queue is clear
