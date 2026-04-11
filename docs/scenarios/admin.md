# NP Admin — Usage Scenarios

# سيناريوهات استخدام — مدير النظام

## Role Overview

- **Title**: System Administrator / مدير النظام
- **CAPS Capabilities**: NP_manage_settings, NP_manage_channels, NP_manage_hooks, NP_manage_routing, NP_manage_integrations
- **Primary DocTypes**: NP Settings, NP Channel, NP Hook Rule, NP Routing Rule, NP Webhook
- **Device**: Desktop

## Daily Scenarios (يومي)

### DS-001: Monitor Channel Health

- **Goal**: Verify all notification channels are operational
- **Steps**:
  1. Navigate to Channels workspace
  2. Review NP Channel Health list — check for any "Down" status
  3. If channel is down, check provider configuration
  4. Verify: All channels show "Healthy" status

### DS-002: Review Failed Notifications

- **Goal**: Identify and resolve delivery failures
- **Steps**:
  1. Navigate to NP Core workspace
  2. Filter NP Notification Log by status = "Failed"
  3. Examine error details per failed notification
  4. Take corrective action (fix template, update channel config)

## Weekly Scenarios (أسبوعي)

### WS-001: Configure New Channel

- **Goal**: Add a new notification channel
- **Steps**:
  1. Navigate to Channels → NP Channel → New
  2. Set channel_name, channel_type, provider configuration
  3. Test channel with a sample notification
  4. Enable channel and assign routing rules

## Monthly Scenarios (شهري)

### MS-001: Review Analytics

- **Goal**: Analyze notification performance across channels
- **Steps**:
  1. Navigate to Analytics workspace
  2. Run Notification Analytics report
  3. Review delivery rates per channel
  4. Adjust routing rules based on performance data
