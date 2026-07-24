
> ### Task 1: Create `vercel.json` with Performance Headers
  
  **Files:**
  - Create: `vercel.json`
  
  **Interfaces:**
  - Consumes: none (standalone)
  - Produces: Vercel deployment config with Cache-Control, security headers
  
  - [ ] **Step 1: Create `vercel.json`**
  
  ```json
  {
    "headers": [
      {
        "source": "/(.*)",
        "headers": [
          { "key": "X-Content-Type-Options", "value": "nosniff" },
          { "key": "X-Frame-Options", "value": "DENY" },
          { "key": "Referrer-Policy", "value": "strict-origin-when-cross-origin" }
        ]
      },
      {
        "source": "/assets/(.*)",
        "headers": [
          { "key": "Cache-Control", "value": "public, max-age=31536000, immutable" }
        ]
      },
      {
        "source": "/css/(.*)",
        "headers": [
          { "key": "Cache-Control", "value": "public, max-age=86400" }
        ]
      },
      {
        "source": "/js/(.*)",
        "headers": [
          { "key": "Cache-Control", "value": "public, max-age=86400" }
        ]
      },
      {
        "source": "\\.(jpg|jpeg|png|webp|svg|ico)$",
        "headers": [
          { "key": "Cache-Control", "value": "public, max-age=31536000, immutable" }
        ]
      }
    ]
  }
  ```
  
  - [ ] **Step 2: Verify file is valid JSON**


