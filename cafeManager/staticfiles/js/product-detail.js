// Product Detail Page JavaScript

// Global variables
let currentQuantity = 1;
let selectedColor = 'Brown';
let selectedSize = 'Medium';

// DOM Elements
const mainImage = document.getElementById('main-product-image');
const quantityDisplay = document.getElementById('quantity');
const thumbnails = document.querySelectorAll('.thumbnail');
const colorOptions = document.querySelectorAll('.color-option');
const sizeOptions = document.querySelectorAll('.size-option');
const selectedOptionSpan = document.querySelector('.selected-option');

// Image Gallery Functions
function changeMainImage(newSrc) {
  // Update main image with high resolution version
  const highResSrc = newSrc.replace('w=150&h=150', 'w=600&h=600');
  mainImage.src = highResSrc;

  // Update thumbnail active state
  thumbnails.forEach(thumb => {
    thumb.classList.remove('active');
    if (thumb.src === newSrc) {
      thumb.classList.add('active');
    }
  });

  // Add smooth transition effect
  mainImage.style.opacity = '0';
  setTimeout(() => {
    mainImage.style.opacity = '1';
  }, 100);
}

// Quantity Controls
function increaseQuantity() {
  if (currentQuantity < 10) { // Max quantity limit
    currentQuantity++;
    updateQuantityDisplay();
  }
}

function decreaseQuantity() {
  if (currentQuantity > 1) { // Min quantity limit
    currentQuantity--;
    updateQuantityDisplay();
  }
}

function updateQuantityDisplay() {
  quantityDisplay.textContent = currentQuantity;

  // Add animation effect
  quantityDisplay.style.transform = 'scale(1.2)';
  setTimeout(() => {
    quantityDisplay.style.transform = 'scale(1)';
  }, 150);
}

// Color Selection
function selectColor(element, color) {
  // Remove active class from all color options
  colorOptions.forEach(option => option.classList.remove('active'));

  // Add active class to selected option
  element.classList.add('active');

  // Update selected color
  selectedColor = color;
  selectedOptionSpan.textContent = color;

  // Add visual feedback
  element.style.transform = 'scale(1.2)';
  setTimeout(() => {
    element.style.transform = 'scale(1.1)';
  }, 150);
}

// Size Selection
function selectSize(element, size) {
  // Remove active class from all size options
  sizeOptions.forEach(option => option.classList.remove('active'));

  // Add active class to selected option
  element.classList.add('active');

  // Update selected size
  selectedSize = size;
}

// Tab Functionality
function showTab(tabName) {
  // Hide all tab contents
  const tabContents = document.querySelectorAll('.tab-content');
  tabContents.forEach(content => {
    content.classList.remove('active');
  });

  // Remove active class from all tab buttons
  const tabButtons = document.querySelectorAll('.tab-btn');
  tabButtons.forEach(btn => {
    btn.classList.remove('active');
  });

  // Show selected tab content
  const selectedTab = document.getElementById(tabName);
  if (selectedTab) {
    selectedTab.classList.add('active');
  }

  // Add active class to clicked tab button
  const clickedButton = event.target;
  clickedButton.classList.add('active');
}

// Add to Cart Function
function addToCart() {
  const cartData = {
    name: 'Designer Handbag',
    price: 299,
    color: selectedColor,
    size: selectedSize,
    quantity: currentQuantity,
    image: mainImage.src
  };

  // Show success message
  showNotification('Product added to cart!', 'success');

  // Update cart count in header
  updateCartCount();

  // Store in localStorage (simple cart implementation)
  let cart = JSON.parse(localStorage.getItem('cart') || '[]');

  // Check if item already exists in cart
  const existingItemIndex = cart.findIndex(item =>
    item.name === cartData.name &&
    item.color === cartData.color &&
    item.size === cartData.size
  );

  if (existingItemIndex > -1) {
    // Update quantity if item exists
    cart[existingItemIndex].quantity += cartData.quantity;
  } else {
    // Add new item to cart
    cart.push(cartData);
  }

  localStorage.setItem('cart', JSON.stringify(cart));
}

// Wishlist Function
function addToWishlist() {
  const wishlistData = {
    name: 'Designer Handbag',
    price: 299,
    image: mainImage.src,
    url: window.location.href
  };

  // Get existing wishlist
  let wishlist = JSON.parse(localStorage.getItem('wishlist') || '[]');

  // Check if item already in wishlist
  const existingItem = wishlist.find(item => item.name === wishlistData.name);

  if (existingItem) {
    showNotification('Already in wishlist!', 'info');
  } else {
    wishlist.push(wishlistData);
    localStorage.setItem('wishlist', JSON.stringify(wishlist));
    showNotification('Added to wishlist!', 'success');
  }
}

// Notification Function
function showNotification(message, type = 'success') {
  // Create notification element
  const notification = document.createElement('div');
  notification.className = `notification ${type}`;
  notification.textContent = message;

  // Style the notification
  notification.style.cssText = `
    position: fixed;
    top: 100px;
    right: 20px;
    background: ${type === 'success' ? '#2ed573' : '#667eea'};
    color: white;
    padding: 15px 25px;
    border-radius: 8px;
    font-weight: 500;
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
    z-index: 1000;
    transform: translateX(100%);
    transition: transform 0.3s ease;
  `;

  // Add to page
  document.body.appendChild(notification);

  // Animate in
  setTimeout(() => {
    notification.style.transform = 'translateX(0)';
  }, 100);

  // Remove after 3 seconds
  setTimeout(() => {
    notification.style.transform = 'translateX(100%)';
    setTimeout(() => {
      document.body.removeChild(notification);
    }, 300);
  }, 3000);
}

// Update Cart Count
function updateCartCount() {
  const cart = JSON.parse(localStorage.getItem('cart') || '[]');
  const totalItems = cart.reduce((sum, item) => sum + item.quantity, 0);

  const cartCountElement = document.querySelector('.cart-count');
  if (cartCountElement) {
    cartCountElement.textContent = totalItems;

    // Add animation
    cartCountElement.style.transform = 'scale(1.3)';
    setTimeout(() => {
      cartCountElement.style.transform = 'scale(1)';
    }, 200);
  }
}

// Initialize Event Listeners
document.addEventListener('DOMContentLoaded', function() {
  // Color option event listeners
  colorOptions.forEach(option => {
    option.addEventListener('click', function() {
      const color = this.getAttribute('data-color');
      selectColor(this, color);
    });
  });

  // Size option event listeners
  sizeOptions.forEach(option => {
    option.addEventListener('click', function() {
      const size = this.getAttribute('data-size');
      selectSize(this, size);
    });
  });

  // Add to cart button
  const addToCartBtn = document.querySelector('.add-to-cart');
  if (addToCartBtn) {
    addToCartBtn.addEventListener('click', addToCart);
  }

  // Wishlist button
  const wishlistBtn = document.querySelector('.wishlist-btn');
  if (wishlistBtn) {
    wishlistBtn.addEventListener('click', addToWishlist);
  }

  // Quantity controls
  const quantityButtons = document.querySelectorAll('.quantity-btn');
  quantityButtons.forEach(btn => {
    btn.addEventListener('click', function() {
      if (this.textContent === '+') {
        increaseQuantity();
      } else if (this.textContent === '-') {
        decreaseQuantity();
      }
    });
  });

  // Tab buttons
  const tabButtons = document.querySelectorAll('.tab-btn');
  tabButtons.forEach(btn => {
    btn.addEventListener('click', function() {
      const tabName = this.textContent.toLowerCase().split(' ')[0];
      showTab(tabName);
    });
  });

  // Initialize cart count
  updateCartCount();

  // Smooth scrolling for anchor links
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      e.preventDefault();
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        target.scrollIntoView({
          behavior: 'smooth',
          block: 'start'
        });
      }
    });
  });

  // Image zoom effect on hover
  if (mainImage) {
    mainImage.addEventListener('mouseenter', function() {
      this.style.transform = 'scale(1.05)';
    });

    mainImage.addEventListener('mouseleave', function() {
      this.style.transform = 'scale(1)';
    });
  }

  // Keyboard navigation for thumbnails
  thumbnails.forEach((thumb, index) => {
    thumb.addEventListener('keydown', function(e) {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        changeMainImage(this.src);
      }
    });

    // Make thumbnails focusable
    thumb.setAttribute('tabindex', '0');
  });

  // Add loading effect to main image
  mainImage.addEventListener('load', function() {
    this.style.opacity = '1';
  });

  // Set initial styles
  mainImage.style.transition = 'all 0.3s ease';
  quantityDisplay.style.transition = 'transform 0.15s ease';
});

// Utility function for price formatting
function formatPrice(price) {
  return '$' + price.toFixed(2);
}

// Function to handle responsive behavior
function handleResponsive() {
  const isMobile = window.innerWidth <= 768;

  if (isMobile) {
    // Mobile-specific adjustments
    const productLayout = document.querySelector('.product-layout');
    if (productLayout) {
      productLayout.style.gap = '30px';
    }
  }
}

// Listen for window resize
window.addEventListener('resize', handleResponsive);

// Call on initial load
handleResponsive();
