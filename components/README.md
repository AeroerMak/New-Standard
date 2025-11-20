# Dynamic Header and Footer System

This project now uses a dynamic component loading system for the header and footer, eliminating code duplication across all HTML pages.

## How It Works

1. **Component Files**: Header and footer HTML are stored in separate files:
   - `components/header.html` - Contains the navigation menu and logo
   - `components/footer.html` - Contains the footer menu and copyright

2. **Loader Script**: `js/components-loader.js` automatically loads these components into pages using JavaScript's Fetch API.

3. **Placeholders**: Each HTML page uses placeholder divs where the header and footer will be inserted:
   - `<div id="header-placeholder"></div>` - For header
   - `<div id="footer-placeholder"></div>` - For footer

## Benefits

- **Single Source of Truth**: Update header/footer once, changes reflect everywhere
- **Easier Maintenance**: No need to update multiple HTML files
- **Consistency**: Ensures all pages have identical header/footer
- **Reduced File Size**: Less code duplication

## Implementation Status

✅ **Completed:**
- `index.html`
- `about.html`

⏳ **Remaining Pages to Update:**
- `collection-badroom.html`
- `collection-dining.html`
- `collection-home.html`
- `collection-kitchen.html`
- `collection-living.html`
- `collection-wallsystems.html`
- `spaces-bedroom.html`
- `spaces-dining.html`
- `spaces-kitchen.html`
- `spaces-living.html`
- `privacy-policy.html`

## How to Update Remaining Pages

For each HTML file, follow these steps:

### Step 1: Replace Header Section
Find the header section (starts with `<div class="header_style_wrapper">`) and replace it with:
```html
<!-- Header will be loaded dynamically here -->
<div id="header-placeholder"></div>
```

### Step 2: Replace Footer Section
Find the footer section (starts with `<div class="footer_bar">`) and replace it along with the hidden inputs with:
```html
<!-- Footer will be loaded dynamically here -->
<div id="footer-placeholder"></div>
```

### Step 3: Add Component Loader Script
Find the first `<script src="js/plugins/jquery.js">` tag and add the component loader BEFORE it:
```html
<!-- Component Loader - Must load before other scripts -->
<script src="js/components-loader.js" type="text/javascript"></script>
<script src="js/plugins/jquery.js" defer="defer" type="text/javascript"></script>
```

## Technical Details

- The loader uses native JavaScript Fetch API (no dependencies)
- Components load asynchronously
- Mobile menu initialization is handled automatically
- Works with existing jQuery-based scripts
- Error handling included (shows error message if component fails to load)

## File Structure

```
/
├── components/
│   ├── header.html      # Header component
│   ├── footer.html      # Footer component
│   └── README.md        # This file
├── js/
│   └── components-loader.js  # Component loader script
└── [all HTML pages]     # Pages using the system
```

## Notes

- The component loader must be loaded BEFORE jQuery (it's placed before jquery.js)
- The loader waits for jQuery to be available before initializing mobile menu
- All paths in component files are relative to the root directory
- The system works with the existing menu.js for mobile menu functionality

