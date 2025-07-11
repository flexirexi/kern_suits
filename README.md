# kern_suits

![Mockup image](doc/img/collage.png)

 # Kern Suits - men 
 Developer: Felix Lehmann<br>
Heroku App: <br>
Github: []()

This project simulates an exclusive suit boutique called _Kern Suits_, which offers high-quality suits and accessories to discerning customers. The platform allows users to purchase products online as well as book personal appointments for tailored fittings and style consultations. 

The website follows a clean and sophisticated design aesthetic intended to communicate elegance while remaining approachable for a modern audience. Because today’s customers expect seamless mobile experiences, the entire project has been built following a mobile-first principle from the start. Moreover, an upcoming recommendation system and a personal profile area will further strengthen customer relationships and brand loyalty.

**The challenges** in this project mainly arose while working with Django’s MVT architecture. Although Django offers powerful abstractions for rapid development, there were several instances where implementing advanced customization required extensive research and experimentation. In particular, integrating Stripe payments with a custom order workflow and extending the user model to store measurement profiles proved to be technically demanding. By contrast, designing the data models for the appointment booking system and product catalog was relatively straightforward.

 **Currently existing user account with multiple bookings**
 - 

 Of course you can also register and test it that way.

**Feel free to register and try it out**

# Kern Suits
---

# Table of content

- [Site Owner Goals](#site-owner-goals)
- [Target Group](#target-group)
- [User Stories](#user-strories)
- [Design & UX](#design-and-ux)
	- [Wireframes](#wireframes)
	- [Colors & Themes](#colors-and-themes)
	- [Mobile First & JavaScript](#mobile-first-and-javascript)
	- [Page Structure & apps](#page-structure-and-apps)
- [Features](#features)
	- [Validations](#validations)
		- [HTML](#html)
		- [CSS](#css)
		- [JS](#js)
		- [PYTHON](#python)
	- [Planned Enhancements](#planned-enhancements)
- [Data & Object Models](#data-and-object-models)
	- [Data Models](#data-models)
	- [Object Models](#object-models)
- [Technologies Used](#technologies-used)
- [SEO & Online Marketing](#seo-and-online-marketing)
	- [SEO](#seo)
	- [Metadata Handling](#metadata-handling)
	- [Online Marketing Strategies](#online-marketing-strategies)
- [Testing & Quality Assurance](#testing-and-quality-assurance)
- [Known Bugs](#known-bugs)
- [Deployment](#deployment)
- [References & Credits](#references-and-credits)


# Site Owner Goals
The main goal of this project is to build a distinctive, premium online presence for Kern Suits that combines modern technology with timeless style. The platform aims to establish a strong brand presence, enable scalable online sales, and integrate personal consultation options to achieve a high conversion rate. Additionally, it is designed to lay the groundwork for effective SEO, including targeted keywords, content marketing, and social media strategies to attract qualified traffic and maintain long-term customer relationships.

---

## Target Group
Kern Suits primarily addresses three main customer segments:

1. **BUSINESS CUSTOMER: Ambitious Professionals**  
    Young and mid-career professionals who invest in quality suits for their daily business life, job interviews, and formal events. They value timeless elegance and appreciate the convenience of online ordering combined with expert personal advice.
    
2. **EVENT CUSTOMER: Style-Conscious Occasion Shoppers**  
    Customers purchasing suits for special occasions such as weddings, gala events, or milestone celebrations. This group is often looking for guidance on fit, styling, and accessories to create a complete and confident look.
    
3. **FASHION CUSTOMER: Style-Conscious Men Who Value Quality**  
	Customers who prioritize high-quality materials, expert tailoring, and a consistent brand experience. They appreciate having their preferences and measurements saved for future purchases, and often engage with the brand through newsletters, exclusive offers, and personal consultations.

---

## User Stories

**As a new Visitor:**
- view a clean and stylish landing page
- see an about page, impressum

**As an authenticated User:**
- I want to register for a personal account, so that I can manage my orders and appointments.
- I want to log in to my personal account, so that I can access my profile and saved data.
- I want to reset my password if forgotten, so that I can regain access to my account.
- I want to edit my personal data (address, contact, size), so that I can receive accurate recommendations and smooth delivery.
- I want to see my order history, so that I can track what I have bought and when it will arrive.
- I want to book a personal appointment, so that I can get expert advice and fitting services.
- I want to manage my upcoming appointments, so that I can reschedule or cancel if needed.
- (optional) I want to delete my account, so that I can remove my data if I no longer wish to use the service.

**As a buyer:**
- I want to browse suits and accessories by size, style, occasion, and fit, so that I can easily find products that match my preferences.
- I want to view detailed product pages with high-quality images and fabric information, so that I can make informed purchase decisions.
- I want to filter and sort products, so that I can quickly narrow down the selection.
- I want to search products by name or category, so that I can locate specific items faster.
- I want to see customer ratings, so that I can gauge the quality and satisfaction levels.
- I want to add items to my shopping cart, so that I can buy multiple products in one transaction.
- I want to edit my cart, so that I can change quantities or remove products before checkout.
- I want to securely check out using Stripe, so that I can pay safely and conveniently.
- (optional) As a customer, I want to receive an email confirmation, so that I have proof of my purchase.
- I want to track my order and delivery status, so that I know when to expect my products.
- I want to review a product after purchase, so that I can share my experience.
- I want to edit or delete my reviews, so that I can update my feedback if necessary.
- (Optional) As a customer, I want to save favorite products to a wishlist, so that I can consider them later.

**As an admin:**
- I want to view all products with CRUD controls, so that I can manage the catalog efficiently.
- I want to add new products, so that I can keep the assortment fresh.
- I want to edit product details, so that I can correct or update information.
- I want to delete products, so that I can remove outdated items.
- I want to manage customer orders and appointments, so that I can ensure smooth operations.
- (Optional) I want to moderate reviews, so that I can maintain content quality.


---

## Design & UX
### Wireframes
*(Insert screenshots or links here)*

### Colors & Theme
- Color palette based on corporate identity
- Dark mode via `data-theme` attribute

### Mobile First & JavaScript
- Fully responsive design
- Progressive enhancement for interactivity

### Page Structure and Apps
- Django app architecture
- Navigation & routing

---

## Features
- Product catalog with filtering and search
- Booking tool with calendar integration
- User profiles with style and measurement data
- Stripe integration for payments
- Admin dashboard

### Validations
- Form input validation
- Booking logic
- Payment validation

### Planned Enhancements
- Recommendation engine
- Voucher and discount modules

---

## Data & Object Models
### Data Models
- Product
- Appointment
- UserProfile
- Order

### Object Models
*(Add UML or diagrams here)*

---

## Technologies Used
- Python, Django
- HTML5, CSS3, JavaScript
- PostgreSQL
- Stripe API
- Bootstrap 5 (optional)

---

## SEO & Online Marketing
### SEO Strategy
- Keyword focus: suits, bespoke tailoring, men's fashion
- On-page SEO: meta tags, alt tags, structured data

### Metadata Handling
- OpenGraph implementation
- Twitter Cards

### Online Marketing Strategies
- Google Ads campaigns
- Social media promotion
- Newsletter automation

---

## Testing & Quality Assurance
- Unit tests
- Functional tests
- Cross-browser and device testing

### Known Bugs
*(Keep this list up to date)*

---

## Deployment
- Heroku deployment steps
- Environment variables
- Static files collection & database migrations

---

## References & Credits
- **Credits:** Project team
- **References:** Django docs, Stripe docs
- **Media:** Unsplash / proprietary photos
- **Acknowledgments:** Supporters & advisors

---

