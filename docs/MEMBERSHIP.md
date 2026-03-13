# Membership System Documentation

## Overview

Complete membership subscription system with payment integration, feature access control, and subscription management.

## Membership Plans

### Monthly - ¥29.9/month
- Unlimited match predictions
- AI-powered analysis
- Advanced data visualization
- Ad-free experience
- Priority support

### Quarterly - ¥79.9/3 months (Save 11%)
- All Monthly features
- Exclusive member badge

### Yearly - ¥299.9/year (Save 16%)
- All Quarterly features
- Early access to new features
- Custom avatar frames

## API Endpoints

### 1. Get Plans
`GET /api/v1/membership/plans`

Returns all available membership plans.

### 2. Subscribe
`POST /api/v1/membership/subscribe`

Create a subscription order.

**Request:**
```json
{
  "plan_id": "monthly",
  "payment_method": "wechat"
}
```

**Response:**
```json
{
  "order_id": "ORD20260313135500ABCD1234",
  "plan_id": "monthly",
  "amount": 29.9,
  "payment_url": "weixin://wxpay/bizpayurl?pr=...",
  "qr_code": "https://api.qrserver.com/v1/create-qr-code/?data=...",
  "expires_at": "2026-03-13T14:25:00Z"
}
```

### 3. Activate Membership
`POST /api/v1/membership/activate/{plan_id}`

Activate membership after payment success (webhook callback).

### 4. Get Status
`GET /api/v1/membership/status`

Get current membership status.

**Response:**
```json
{
  "is_member": true,
  "member_type": "yearly",
  "expire_at": "2027-03-13T13:40:00Z",
  "days_remaining": 365,
  "features": [
    "unlimited_predictions",
    "ai_analysis",
    "advanced_charts",
    "no_ads",
    "priority_support",
    "exclusive_badge",
    "early_access",
    "custom_avatar"
  ]
}
```

### 5. Check Feature Access
`GET /api/v1/membership/check-feature/{feature_key}`

Check if user has access to a specific feature.

**Response:**
```json
{
  "feature_key": "ai_analysis",
  "is_available": true,
  "reason": null
}
```

### 6. Cancel Membership
`POST /api/v1/membership/cancel`

Cancel membership (will expire at end of current period).

## Feature Access Control

### Backend Usage

```python
from app.services.membership_service import MembershipService

async def some_protected_endpoint(
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    service = MembershipService(db)
    feature = await service.check_feature(current_user.id, "ai_analysis")
    
    if not feature.is_available:
        raise HTTPException(
            status_code=403,
            detail=f"Feature not available: {feature.reason}"
        )
    
    # Proceed with feature logic
    ...
```

### Frontend Usage

```vue
<script setup>
import { ref, onMounted } from 'vue'
import { api } from '@/api'

const membershipStatus = ref(null)

onMounted(async () => {
  membershipStatus.value = await api.get('/membership/status')
})

async function checkFeature(featureKey) {
  const result = await api.get(`/membership/check-feature/${featureKey}`)
  return result.is_available
}
</script>

<template>
  <div v-if="membershipStatus?.is_member" class="member-badge">
    <span>{{ membershipStatus.member_type }} Member</span>
    <span>{{ membershipStatus.days_remaining }} days remaining</span>
  </div>
  
  <button
    v-if="!membershipStatus?.is_member"
    @click="showSubscribeModal"
  >
    Upgrade to Premium
  </button>
</template>
```

## Payment Integration

### Supported Payment Methods

1. **WeChat Pay** (`wechat`)
   - QR code payment
   - In-app payment (WeChat mini-program)

2. **Alipay** (`alipay`)
   - QR code payment
   - Web payment

3. **Stripe** (`stripe`)
   - Credit/debit cards
   - International payments

### Payment Flow

```
1. User selects plan
   ↓
2. POST /membership/subscribe
   ↓
3. Get payment URL/QR code
   ↓
4. User completes payment
   ↓
5. Payment gateway webhook
   ↓
6. POST /membership/activate/{plan_id}
   ↓
7. Membership activated
```

### Webhook Configuration

**WeChat Pay:**
```
Webhook URL: https://your-domain.com/api/v1/webhooks/wechat
```

**Alipay:**
```
Notify URL: https://your-domain.com/api/v1/webhooks/alipay
```

**Stripe:**
```
Webhook URL: https://your-domain.com/api/v1/webhooks/stripe
Events: checkout.session.completed
```

## Database Schema

User table already has membership fields (from migration 002):
- `is_member` (boolean)
- `member_type` (string: monthly/quarterly/yearly)
- `member_expire_at` (datetime)

## Security

### Payment Security
- All payment data handled by payment gateways
- No credit card info stored on server
- HTTPS required for all payment endpoints

### Feature Access
- Check membership status on every protected endpoint
- Validate expiration date
- Cache membership status (5 minutes)

## Testing

### Test Subscription Flow

```bash
# 1. Get plans
curl http://localhost:8000/api/v1/membership/plans

# 2. Subscribe (requires auth token)
curl -X POST http://localhost:8000/api/v1/membership/subscribe \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"plan_id": "monthly", "payment_method": "wechat"}'

# 3. Activate (for testing, skip payment)
curl -X POST http://localhost:8000/api/v1/membership/activate/monthly \
  -H "Authorization: Bearer YOUR_TOKEN"

# 4. Check status
curl http://localhost:8000/api/v1/membership/status \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## Future Enhancements

- [ ] Auto-renewal management
- [ ] Refund handling
- [ ] Subscription analytics
- [ ] Promotional codes/discounts
- [ ] Gift memberships
- [ ] Family plans
- [ ] Trial periods

---

**Version:** v1.0  
**Last Updated:** 2026-03-13
