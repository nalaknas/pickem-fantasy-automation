# SMS Notifications Feature

## Overview

The SMS notifications feature automatically sends weekly skins game results to your group chat via Twilio SMS. This feature includes:

- **Confirmation prompts** before sending messages
- **Test functionality** to verify SMS setup
- **Flexible recipient management** for group chats
- **Rich message formatting** with emojis and clear results

## Setup

### 1. Install Twilio Package

```bash
pip install twilio
```

Or install all requirements:
```bash
pip install -r requirements.txt
```

### 2. Get Twilio Credentials

1. Sign up for Twilio at https://www.twilio.com/
2. Go to the [Twilio Console](https://console.twilio.com/)
3. Get your **Account SID** and **Auth Token**
4. Purchase a phone number for sending SMS

### 3. Configure Environment Variables

Add these to your `.env` file:

```bash
# Twilio Configuration
TWILIO_ACCOUNT_SID=your_account_sid_here
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_FROM_NUMBER=+1234567890
TWILIO_TO_NUMBERS=+1234567890,+0987654321,+15551234567
```

**Note**: Use `+` prefix for all phone numbers (e.g., `+1234567890`)

## Testing

### Quick Test

```bash
python3 test_sms.py
```

### Test with Specific Numbers

```bash
python3 test_sms.py +1234567890
python3 test_sms.py +1234567890,+0987654321
```

### Test via Main Script

```bash
python3 main.py test-sms
python3 main.py test-sms +1234567890
```

## Usage

### Weekly Processing with SMS

1. Process a week normally:
   ```bash
   python3 main.py
   ```

2. The system will ask if you want to send SMS notifications:
   ```
   📱 SMS NOTIFICATIONS
   ==============================
   ✅ SMS notifications configured
   📞 Configured numbers: ['+1234567890', '+0987654321']
   
   🤔 Send SMS notifications to group chat? (y/N):
   ```

3. If you choose `y`, you'll see a message preview and confirmation:
   ```
   📝 Message preview:
   ----------------------------------------
   🏈 A League of Buddies Pool - Week 1 Results 🏈
   
   🥇 HIGHEST SCORER: John
   Score: 12.0 points
   
   🥈 SECOND HIGHEST: Sarah
   Score: 10.0 points
   
   🥉 THIRD HIGHEST: Mike
   Score: 8.0 points
   
   📉 LOWEST SCORER: Tom
   Score: 2.0 points
   
   Season 2025 • Week 1
   Good luck next week! 🍀
   ----------------------------------------
   
   🤔 Send this message? (y/N):
   ```

## Message Format

SMS messages include:

- **League name and week number**
- **Highest scorer** with points
- **Second highest scorer** (if applicable)
- **Third highest scorer** (if applicable)
- **Lowest scorer** with points
- **No picks submitted** (if applicable)
- **Perfect week winners** (if any)
- **Season and week info**

## Configuration Options

### Multiple Recipients

Add multiple phone numbers separated by commas:

```bash
TWILIO_TO_NUMBERS=+1234567890,+0987654321,+15551234567
```

### Group Chat Support

SMS notifications work with any phone numbers, including group chat numbers. Just add the group chat number to your `TWILIO_TO_NUMBERS` list.

## Troubleshooting

### Common Issues

1. **"SMS not configured"**
   - Check your `.env` file has all Twilio variables
   - Verify Account SID and Auth Token are correct

2. **"Failed to send notification"**
   - Check phone number format (must include `+` prefix)
   - Verify Twilio account has sufficient credits
   - Ensure the from number is verified in Twilio

3. **"Twilio package not installed"**
   - Run: `pip install twilio`

### Testing Steps

1. **Test Twilio credentials**:
   ```bash
   python3 test_sms.py
   ```

2. **Test with your phone number**:
   ```bash
   python3 test_sms.py +YOUR_PHONE_NUMBER
   ```

3. **Test group chat number**:
   ```bash
   python3 test_sms.py +GROUP_CHAT_NUMBER
   ```

## Security Notes

- **Never commit your `.env` file** to version control
- **Keep Twilio credentials secure**
- **Use environment variables** for all sensitive data
- **Test with small amounts** before using in production

## Cost Considerations

- Twilio charges per SMS sent
- Check Twilio pricing at https://www.twilio.com/pricing
- Consider message length limits (SMS has 160 character limit per segment)

## Future Enhancements

- **Scheduled sending** (Tuesday morning automation)
- **Message templates** for different result types
- **Delivery status tracking**
- **Multiple message formats** (short/long versions)
