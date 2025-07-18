# kern_suits

![Mockup image](doc/mockup.jpg)

 # Kern Suits - menswear
 Developer: Felix Lehmann<br>
Render App: https://kern-suits.onrender.com/<br>
Github: [Kern Suits](https://github.com/flexirexi/kern_suits)

This project simulates an exclusive suit boutique called _Kern Suits_, which offers high-quality suits and accessories to discerning customers. The platform allows users to purchase products online as well as book personal appointments for tailored fittings and style consultations. 

The website follows a clean and sophisticated design aesthetic intended to communicate elegance while remaining approachable for a modern audience. Because today’s customers expect seamless mobile experiences, the entire project has been built following a mobile-first principle from the start. Moreover, an upcoming recommendation system and a personal profile area will further strengthen customer relationships and brand loyalty.

**The challenges** in this project mainly arose while working with Django’s MVT architecture. Although Django offers powerful abstractions for rapid development, there were several instances where implementing advanced customization required extensive research and experimentation. In particular, integrating Stripe payments with a custom order workflow and extending the user model to store measurement profiles proved to be technically demanding. By contrast, designing the data models for the appointment booking system and product catalog was relatively straightforward.

 **Currently existing user account with multiple bookings**

 - an admin account will be given personally to CI
 - other accounts and profiles can be set up by simply signing up to this page.


**Feel free to try it out**

# Kern Suits
---

# Table of content

- [Site Owner Goals](#site-owner-goals)
- [Target Group](#target-group)
- [SEO & Online Marketing](#seo-and-online-marketing)
	- [SEO](#seo-strategy)
	- [Metadata Handling](#metadata-handling)
	- [Online Marketing Strategies](#online-marketing-strategies)
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
- [Data Models](#data-models)
	- [Data Models](#data-models)
- [Technologies Used](#technologies-used)
- [Accessibility](#accessibility)
- [Testing & Quality Assurance](#testing-and-quality-assurance)
   - [Automated Testing](#automated-testing)
      - [JavaScript (Jest)]()
	  - [Python](#python)
   - [Manual Testing](#manual-testing)
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

## SEO and Online Marketing
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

**please note**: SEO is not yet available!

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
- I can see an order confirmation after checkout, so that I can be assured that everything went well
- (optional) As a customer, I want to receive an email confirmation, so that I have proof of my purchase.
- I want to track my order and delivery status, so that I know when to expect my products.
- I want to review a product after purchase, so that I can share my experience.
- I want to edit or delete my reviews, so that I can update my feedback if necessary.
- (Optional) As a customer, I want to save favorite products to a wishlist, so that I can consider them later.

---
(not done yet:)
**As an admin:**
- I want to view all products with CRUD controls, so that I can manage the catalog efficiently.
- I want to add new products, so that I can keep the assortment fresh.
- I want to edit product details, so that I can correct or update information.
- I want to delete products, so that I can remove outdated items.
- I want to manage customer orders and appointments, so that I can ensure smooth operations.
- (Optional) I want to moderate reviews, so that I can maintain content quality.


---

## Design and UX
### Wireframes

Wireframes provide a basic idea how to structure and design your templates. My wireframes look very simple but they also serve this very one purpose: the layout. Themes and colors can (even drastically) change during the development process. Also, I tried not to repeat myself (DRY-principle), so, you'll find a sufficient collection of wireframes for this project. 


**landing page and similar templates within the home app**

<img src="doc/img/wireframes/wf_home.png" width="500px">


**products page from the products-app**

<img src="doc/img/wireframes/wf_products.png" width="500px">


**products_details page from the products-app**

<img src="doc/img/wireframes/wf_product_details.png" width="500px">


**shopping bag from the bag-app**

<img src="doc/img/wireframes/wf_shopping_bag.png" width="500px">


**checkout page from the checkout-app**

<img src="doc/img/wireframes/wf_checkout.png" width="500px">


**appointments page from the appointment-app**

<img src="doc/img/wireframes/wf_appointments.png" width="500px">

- please note: I altered the layout a bit because the necessary information for tailoring appointments can be done in a few sentences on the landing page
- so, the appointment page is directly a booking tool for timeslots

### Colors and Theme
My color and theme architecture is built on some principles, prioritizing clarity, maintainability, and full control over visual styling across themes - even with Bootstrap.

#### Core Approach:

- **CSS Variables (`:root` and `[data-theme]`)**  
  All theme colors are defined as custom properties, scoped by `data-theme` (e.g., `html[data-theme]`). This makes theme switching and overwriting instant and modular.

- **Structural Specificity without `!important`**  
  By using clear scoping via `[data-theme]`, `!important`-overrides become unnecessary. This eliminates style conflicts and improves maintainability—especially when scaling up. The beauty of this is that `[data-theme]` creates a higher priority than the bootstrap classes -> that means I can alter the "btn-danger" color with no effort, if I want. It's like an add-on.

- **Bootstrap Compatibility by Extension**  
  Bootstrap is not overwritten directly. Instead, custom variables are injected via `themes.css` and `themes.css` to align with Bootstrap’s internal system. This ensures compatibility with future updates and plugins.

- **Clear Separation of Concerns**  
  `themes.css` holds all visual design tokens (colors, radii, etc.), while `layout.css` handles structural spacing and layout constants, such as nav-height, general paddings etc. This keeps design logic clean and reusable.

- **Cross-Browser Transparency Handling**  
  We avoid problematic `#hexAlpha` syntax (e.g., `#ffffff80`) and use `rgba(...)` for alpha values. Colors without alphas are in hex-method. This ensures consistent rendering, especially in Safari and mobile WebKit engines.


#### Why this approach:

- **Scalability** – Easily supports future color modes, themes or branding variants without architectural changes.
- **Predictability** – Reduces CSS conflicts, making the styling layer easier to debug and collaborate on.
- **Maintainability** – Encourages a consistent design system with minimal coupling between code and visuals. Moreover, other coders could easily adapt and maintain in the future.
- **Performance** – Theme switching has zero layout cost and minimal DOM operations.
- **Professionalism** – Clean code structure mirrors industry standards and makes onboarding faster for collaborators.


### Mobile First & JavaScript

Our frontend follows a strict mobile-first and progressively enhanced JavaScript approach. This ensures functionality and performance across all devices and bandwidth conditions.


#### Core Principles:

- **Mobile-First Design**  
  Layouts are built from the smallest viewport upward. This guarantees optimal performance and usability on mobile, then enhances for tablets and desktops. Thanks to Bootstrap, this approach nearly happens automatically.

- **Progressive Enhancement**  
  Core functionality (navigation, content access, forms) works without JavaScript. Interactive features are layered on top, improving user experience without compromising accessibility. I like to add here: No JS is better than good JS. This is not an argument against JS - it actually is for JS. Use JS for the complicated "in-between" solutions that neither the backend nor html/CSS can solve elegantly.

- **Modular JS Components**  
  JavaScript is cleanly structured and scope-safe. DOM manipulation is targeted and event-driven, following best practices to avoid global leakage. Each script gets their own JS file in their own app's static directory. Scripts can become chaotic very quickly, for instance the stripe script.

- **Performance-Oriented**  
  No unnecessary libraries are loaded. Vanilla JS is preferred where possible. Event listeners are delegated and optimized for responsiveness. An exception is JQuery. Initially, it was used for stripe until I needed to re-write it to vanilla JS.

- **Responsiveness is Testable and Reliable**  
  All breakpoints and flex/grid logic are verified with Chrome DevTools and physical devices.

This approach aligns with modern development standards and ensures consistent behavior across environments—especially in a professional production context. There are still some minor design/layout issues but they are caused by the complexity of collectstatic and deployment.


### Page Structure and Apps
- Django app architecture
- Navigation & routing
- not yet done!

---

## Features
- Product catalog with filtering and search
- Booking tool with calendar integration
- User profiles with style and measurement data
- Stripe integration for payments
- Admin dashboard
- not yet done (writing this)

## Validations
- Form input validation
- Booking logic
- Payment validation
- not yet done!

### Planned Enhancements
- a custom product admin app with CRUD functionalities to manage products in the store
- email notifications are not in place yet
- SEO is not in place yet

---

## Data and Object Models
### Data Models

### products: Category

| Key | Name   | Type             |
| --- | ------ | ---------------- |
|     | `name` | `CharField[100]` |
|     | `slug` | `SlugField`      |


### products: Series

| Key | Name          | Type             |
| --- | ------------- | ---------------- |
|     | `name`        | `CharField[100]` |
|     | `slug`        | `SlugField`      |
|     | `description` | `TextField`      |
|     | `is_active`   | `BooleanField`   |


### products: Occasion

| Key | Name   | Type             |
| --- | ------ | ---------------- |
|     | `name` | `CharField[100]` |
|     | `slug` | `SlugField[100]` |


### products: Product 

| Key | Name          | Type                           |
| --- | ------------- | ------------------------------ |
|     | `category`    | `ForeignKey(Category)`         |
|     | `occasion`    | `ForeignKey(Occasion)`         |
|     | `series`      | `ForeignKey(Series)`           |
|     | `name`        | `CharField[255]`               |
|     | `slug`        | `SlugField`                    |
|     | `description` | `TextField`                    |
|     | `fabric`      | `CharField[100]`               |
|     | `is_active`   | `BooleanField`                 |
|     | `image_url`   | `URLField[1024]` (nullable)    |
|     | `image`       | `ImageField` (nullable)        |
|     | `rating`      | `DecimalField(6,2)` (nullable) |

- please note: the product acts more like a category for the actual product variants which differ by size, color and fit and, technkically by price


### products: Size

| Key | Name   | Type            |
| --- | ------ | --------------- |
|     | `name` | `CharField[40]` |
|     | `kind` | `CharField[40]` |


### products: Fit

| Key | Name   | Type                     |
| --- | ------ | ------------------------ |
|     | `name` | `CharField[40]` (unique) |
|     | `slug` | `SlugField[40]`          |


### products: Color

| Key | Name       | Type                     |
| --- | ---------- | ------------------------ |
|     | `name`     | `CharField[40]` (unique) |
|     | `slug`     | `SlugField[40]`          |
|     | `hex_code` | `CharField[10]`          |


### products: ProductVariant

| Key | Name        | Type                           |
| --- | ----------- | ------------------------------ |
|     | `product`   | `ForeignKey(Product)`          |
|     | `size`      | `ForeignKey(Size)`             |
|     | `fit`       | `ForeignKey(Fit)`              |
|     | `color`     | `ForeignKey(Color)`            |
|     | `sku`       | `CharField[50]` (unique)       |
|     | `stock`     | `PositiveIntegerField`         |
|     | `price`     | `DecimalField(8,2)` (nullable) |
|     | `is_active` | `BooleanField`                 |

- this is the "actual" product. that, what the customer can order


### appointments: Appointment

| Key | Name               | Type                       |
| --- | ------------------ | -------------------------- |
|     | `user`             | `ForeignKey(User)`         |
|     | `start_datetime`   | `DateTimeField`            |
|     | `end_datetime`     | `DateTimeField` (nullable) |
|     | `appointment_type` | `CharField[20]` (choices)  |
|     | `comment`          | `TextField` (nullable)     |


### checkout: Order

| Key        | Name             | Type                              |
| ---------- | ---------------- | --------------------------------- |
| PrimaryKey | `order_number`   | `CharField[32]` (UUID, unique)    |
| FK         | `user`           | `ForeignKey(User)`                |
|            | `created_at`     | `DateTimeField(auto_now_add)`     |
|            | `updated_at`     | `DateTimeField(auto_now)`         |
|            | `status`         | `CharField[20]` (choice field)    |
|            | `first_name`     | `CharField[100]`                  |
|            | `last_name`      | `CharField[100]`                  |
|            | `email`          | `EmailField`                      |
|            | `phone`          | `CharField[20]` (optional)        |
|            | `address_line1`  | `CharField[255]`                  |
|            | `address_line2`  | `CharField[255]` (optional)       |
|            | `postal_code`    | `CharField[20]`                   |
|            | `city`           | `CharField[100]`                  |
|            | `country`        | `CountryField` (django-countries) |
|            | `total_amount`   | `DecimalField[10,2]`              |
|            | `delivery_costs` | `DecimalField[10,2]`              |
|            | `grand_total`    | `DecimalField[10,2]`              |
|            | `stripe_pid`     | `CharField[255]` (optional)       |
|            | `original_bag`   | `TextField` (optional)            |


### checkout: OrderItem

| Key | Name       | Type                         |
| --- | ---------- | ---------------------------- |
| FK  | `order`    | `ForeignKey(Order)`          |
| FK  | `variant`  | `ForeignKey(ProductVariant)` |
|     | `quantity` | `PositiveIntegerField`       |
|     | `price`    | `DecimalField[10,2]`         |


### reviews: Review

| Key | Name         | Type                          |
| --- | ------------ | ----------------------------- |
| FK  | `user`       | `ForeignKey(User)`            |
| FK  | `product`    | `ForeignKey(Product)`         |
|     | `rating`     | `FloatField`                  |
|     | `comment`    | `TextField` (optional)        |
|     | `created_at` | `DateTimeField(auto_now_add)` |


### user: UserProfile

| Key | Name              | Type                      |
| --- | ----------------- | ------------------------- |
| FK  | `user`            | `OneToOneField(User)`     |
|     | `phone_number`    | `CharField` (optional)    |
|     | `street_address1` | `CharField` (optional)    |
|     | `street_address2` | `CharField` (optional)    |
|     | `town_or_city`    | `CharField` (optional)    |
|     | `county`          | `CharField` (optional)    |
|     | `postcode`        | `CharField` (optional)    |
|     | `country`         | `CountryField` (optional) |


### user: StyleProfile

| Key | Name                | Type                                |
| --- | ------------------- | ----------------------------------- |
| FK  | `user_profile`      | `OneToOneField(UserProfile)`        |
| FK  | `jacket_size`       | `ForeignKey(Size)` *(optional)*     |
| FK  | `shirt_size`        | `ForeignKey(Size)` *(optional)*     |
| FK  | `trousers_size`     | `ForeignKey(Size)` *(optional)*     |
| FK  | `waistcoat_size`    | `ForeignKey(Size)` *(optional)*     |
| FK  | `belt_size`         | `ForeignKey(Size)` *(optional)*     |
| FK  | `preferred_color_1` | `ForeignKey(Color)` *(optional)*    |
| FK  | `preferred_color_2` | `ForeignKey(Color)` *(optional)*    |
| FK  | `preferred_color_3` | `ForeignKey(Color)` *(optional)*    |
| FK  | `fit_preference`    | `ForeignKey(Fit)` *(optional)*      |
| FK  | `occasion_1`        | `ForeignKey(Occasion)` *(optional)* |
| FK  | `occasion_2`        | `ForeignKey(Occasion)` *(optional)* |
| FK  | `occasion_3`        | `ForeignKey(Occasion)` *(optional)* |

- please note: styles are not yet used in the project. It is supposed to be used for email marketing when certain sizes are available again.




## Technologies Used

### Libraries & Tools

- [Am I Responsive](http://ami.responsivedesign.is/)
- [Balsamiq](https://balsamiq.com/)
- [Bootstrap v5.3](https://getbootstrap.com/docs/5.3/getting-started/introduction/)
- [Favicon.io](https://favicon.io/)
- [Chrome DevTools](https://developer.chrome.com/docs/devtools/)
- [Font Awesome](https://fontawesome.com/)
- [Git](https://git-scm.com/)
- [GitHub](https://github.com/)
- [Google Fonts](https://fonts.google.com/)
- [Render Platform](https://www.render.com/) *(legacy deployment)*
- [AWS](https://aws.amazon.com/)
- [jQuery](https://jquery.com/) *(it was integrated for stripe - but then i re-wrote it..)*
- [PostgreSQL](https://www.postgresql.org/)
- [Summernote](https://summernote.org/)


### Languages & Frameworks

- [HTML](https://developer.mozilla.org/en-US/docs/Web/HTML)
- [CSS](https://developer.mozilla.org/en-US/docs/Web/CSS)
- [JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
- [Python](https://www.python.org/)
- [Django](https://www.djangoproject.com/)
---

## Accessibility
- not yet done!

---

## Testing and Quality Assurance

### Automated Testing

#### Python 

#### App: "appointment"
<details>
<summary>views testing - OK</summary>
<img src="doc/img/testing/python/appt_ok.png" width="500px">
</details>

#### App: "bag"
<details>
<summary>views testing - OK</summary>
<img src="doc/img/testing/python/bag_ok.png" width="500px">
</details>

<details>
<summary>bag context processor testing - OK</summary>
<img src="doc/img/testing/python/bag_context_ok.png" width="500px">
</details>

#### App: "checkout"
<details>
<summary>views testing - OK</summary>
<img src="doc/img/testing/python/checkout_view_ok.png" width="500px">
</details>

<details>
<summary>models testing - OK</summary>
<img src="doc/img/testing/python/checkout_models_ok.png" width="500px">
</details>

#### App: "products"
<details>
<summary>views testing - OK</summary>
<img src="doc/img/testing/python/products_views_ok.png" width="500px">
</details>

<details>
<summary>ratings testing - OK</summary>
<img src="doc/img/testing/python/products_ratings_ok.png" width="500px">
</details>

| Feature      | Action                        | Expected Result                              | Actual Result        |
|--------------|-------------------------------|-----------------------------------------------|----------------------|
| Landing Page | Load homepage as new visitor | Brand appears premium and stylish            | Works as expected    |

### Manual Testing

<h4 style="color: yellow;">As a new visitor</h4>

#### Test 1

<details>
<summary>As a new visitor: I want to view a clean and stylish landing page, so that I can immediately understand the brand’s quality and style</summary>
<img src="doc/img/testing/manual/01.png" width="400px">
</details>


| Feature      | Action                        | Expected Result                              | Actual Result        |
|--------------|-------------------------------|-----------------------------------------------|----------------------|
| Landing Page | Load homepage as new visitor | Brand appears premium and stylish            | Works as expected    |



#### Test 2

<details>
<summary>As a new visitor: I want to see an about page and legal information, so that I can trust the company before making a purchase</summary>
<img src="doc/img/testing/manual/02.png" width="400px">
</details>


| Feature       | Action                    | Expected Result                             | Actual Result        |
|---------------|---------------------------|----------------------------------------------|----------------------|
| About & Legal | Access about/legal pages  | Transparency builds trust                    | Works as expected    |


<h4 style="color: yellow;">As an authenticated User</h4>

#### Test 3

<details>
<summary>As an authenticated user: I want to register for a personal account, so that I can manage my orders and appointments</summary>
<img src="doc/img/testing/manual/03.png" width="400px">
</details>


| Feature             | Action                    | Expected Result                                      | Actual Result        |
|---------------------|---------------------------|------------------------------------------------------|----------------------|
| User Registration   | Register new user account | Account is successfully created and ready to use    | Works as expected    


#### Test 4

<details>
<summary>As an authenticated user: I want to log in to my personal account, so that I can access my profile and saved data</summary>
<img src="doc/img/testing/manual/04.png" width="400px">
</details>


| Feature   | Action           | Expected Result                           | Actual Result        |
|-----------|------------------|--------------------------------------------|----------------------|
| Login     | Log into account | Access to profile and stored user data     | Works as expected    |


#### _Test 5_

<details>
<summary>As an authenticated user: I want to reset my password if forgotten, so that I can regain access to my account</summary>
<img src="doc/img/testing/manual/05.png" width="400px">
</details>


| Feature         | Action                 | Expected Result                                      | Actual Result        |
|-----------------|------------------------|------------------------------------------------------|----------------------|
| Password Reset  | Trigger password reset | Email with reset link is sent                       | email wont be sent!    |

**NOTE:** An actual email is not been sent to 

#### Test 6

<details>
<summary>As an authenticated user: I want to edit my personal data (address, contact, size), so that I can receive accurate recommendations and smooth delivery</summary>
<img src="doc/img/testing/manual/06.png" width="400px">
</details>


| Feature           | Action                     | Expected Result                                           | Actual Result        |
|-------------------|----------------------------|------------------------------------------------------------|----------------------|
| Profile Settings  | Edit address/contact/size  | Personalized recommendations and correct delivery          | Works as expected    |



#### Test 7

<details>
<summary>As an authenticated user: I want to see my order history, so that I can track what I have bought and when it will arrive</summary>
<img src="doc/img/testing/manual/07.png" width="400px">
</details>


| Feature       | Action             | Expected Result                                     | Actual Result        |
|----------------|--------------------|-----------------------------------------------------|----------------------|
| Order History | View past orders   | Overview of past purchases and expected delivery    | Works as expected    |


<h4 style="color: yellow;">As a buyer</h4>

#### Test 8

<details>
<summary>As an authenticated user: I want to book a personal appointment, so that I can get expert advice and fitting services</summary>
<img src="doc/img/testing/manual/08.png" width="400px">
</details>


| Feature              | Action                    | Expected Result                                           | Actual Result        |
|----------------------|---------------------------|------------------------------------------------------------|----------------------|
| Appointment Booking  | Book personal appointment | Appointment is scheduled with expert support              | Works as expected    |



#### Test 9

<details>
<summary>As an authenticated user: I want to manage my upcoming appointments, so that I can reschedule or cancel if needed</summary>
<img src="doc/img/testing/manual/09.png" width="400px">
</details>


| Feature                | Action                         | Expected Result                                       | Actual Result        |
|------------------------|--------------------------------|--------------------------------------------------------|----------------------|
| Appointment Management | View/edit upcoming appointments| Appointments can be updated or canceled                | Works as expected    |



#### Test 10

<details>
<summary>As a buyer: I want to browse suits and accessories by size, category, occasion, fit, fabric, color and collection name, so that I can easily find products that match my preferences</summary>
<img src="doc/img/testing/manual/10.png" width="400px">
</details>


| Feature          | Action                        | Expected Result                                                  | Actual Result        |
|------------------|-------------------------------|-------------------------------------------------------------------|----------------------|
| Product Browsing | Use filters to explore catalog| Products are displayed according to selected preferences         | Works as expected    |



#### Test 11

<details>
<summary>As a buyer: I want to view detailed product pages with high-quality images and fabric/ occasion/ color/ size/ fit/ series name/ price information, so that I can make informed purchase decisions</summary>
<img src="doc/img/testing/manual/11.png"   width="600px">

<img src="doc/img/testing/manual/11_2.png" width="600px">

<img src="doc/img/testing/manual/11_3.png" width="600px">

<img src="doc/img/testing/manual/11_4.png" width="600px">

</details>


| Feature         | Action                  | Expected Result                                                     | Actual Result        |
|-----------------|-------------------------|----------------------------------------------------------------------|----------------------|
| Product Details | Open product detail page| Detailed information and images are clearly displayed                | Works as expected    |



#### Test 12

<details>
<summary>As a buyer: I want to filter and sort products, so that I can quickly narrow down the selection</summary>
<img src="doc/img/testing/manual/12.png" width="600px">
<img src="doc/img/testing/manual/12_2.png" width="600px">
<img src="doc/img/testing/manual/12_3.png" width="600px">
</details>

| Feature         | Action              | Expected Result                                         | Actual Result        |
|-----------------|---------------------|----------------------------------------------------------|----------------------|
| Product Filter  | Apply filters/sorting| Product list updates according to selected options       | Works as expected    |


#### Test 13

<details>
<summary>As a buyer: I want to search products by name or category, so that I can locate specific items faster</summary>
<img src="doc/img/testing/manual/13.png" width="600px">
<img src="doc/img/testing/manual/13_2.png" width="600px">
</details>

| Feature         | Action             | Expected Result                                | Actual Result        |
|-----------------|--------------------|-------------------------------------------------|----------------------|
| Product Search  | Use search function| Matching products are shown in search results   | Works as expected    |

**PLEASE NOTE:** this user story seems redundant but after a certain time i realized: you dont only want to filter the products, you also want to see information (eg. occasion, series name etc)..

#### Test 14

<details>
<summary>As a buyer: I want to see customer ratings, so that I can gauge the quality and satisfaction levels</summary>
<img src="doc/img/testing/manual/14.png" width="400px">
</details>


| Feature          | Action               | Expected Result                                  | Actual Result        |
|------------------|----------------------|---------------------------------------------------|----------------------|
| Product Ratings  | View customer reviews| Displayed reviews give insights into satisfaction | Works as expected    |



#### Test 15

<details>
<summary>As a buyer: I want to add items to my shopping cart, so that I can buy multiple products in one transaction</summary>
<img src="doc/img/testing/manual/15.png" width="400px">
</details>

| Feature         | Action             | Expected Result                                       | Actual Result        |
|-----------------|--------------------|--------------------------------------------------------|----------------------|
| Shopping Cart   | Add item to cart   | Product is added and cart reflects correct contents   | Works as expected    |


#### Test 16

<details>
<summary>As a buyer: I want to edit my cart, so that I can change quantities or remove products before checkout</summary>
<img src="doc/img/testing/manual/16.png" width="400px">
</details>

| Feature        | Action                    | Expected Result                                         | Actual Result        |
|----------------|---------------------------|----------------------------------------------------------|----------------------|
| Cart Editing   | Update/remove item in cart| Cart updates accordingly                                 | Works as expected    |


#### Test 17

<details>
<summary>As a buyer: I want to securely check out using Stripe, so that I can pay safely and conveniently</summary>
<img src="doc/img/testing/manual/17.png" width="400px">
</details>

| Feature     | Action             | Expected Result                            | Actual Result        |
|--------------|--------------------|---------------------------------------------|----------------------|
| Checkout     | Pay via Stripe     | Secure payment is completed successfully   | Works as expected    |


#### Test 18

<details>
<summary>As a buyer: I can see an order confirmation after checkout, so that I can be assured that everything went well</summary>
<img src="doc/img/testing/manual/18.png" width="400px">
</details>

| Feature              | Action            | Expected Result                                       | Actual Result        |
|----------------------|-------------------|--------------------------------------------------------|----------------------|
| Order Confirmation   | Finish checkout   | Confirmation message and order summary are displayed  | Works as expected    |


#### _Test 19_ (optional)

<details>
<summary>As a customer: I want to receive an email confirmation, so that I have proof of my purchase</summary>
<img src="doc/img/testing/manual/19.png" width="400px">
</details>

| Feature              | Action                  | Expected Result                                  | Actual Result        |
|----------------------|-------------------------|--------------------------------------------------|----------------------|
| Email Confirmation   | Check inbox after order | Email receipt with order details is received    | Not yet in place!    |


#### Test 20

<details>
<summary>As a buyer: I want to track my order and delivery status, so that I know when to expect my products</summary>
<img src="doc/img/testing/manual/20.png" width="400px">
</details>


| Feature         | Action               | Expected Result                                | Actual Result        |
|-----------------|----------------------|------------------------------------------------|----------------------|
| Order Tracking  | View delivery status | Current shipping and delivery status visible   | Works as expected    |


#### Test 21

<details>
<summary>As a buyer: I want to review a product after purchase, so that I can share my experience</summary>
<img src="doc/img/testing/manual/21.png" width="600px">
<img src="doc/img/testing/manual/21_2.png" width="600px">
</details>

| Feature        | Action              | Expected Result                                         | Actual Result        |
|----------------|---------------------|----------------------------------------------------------|----------------------|
| Product Review | Submit review form  | Review is saved and shown on the product page          | Works as expected    |


#### Test 22

<details>
<summary>As a buyer: I want to edit or delete my reviews, so that I can update my feedback if necessary</summary>
<img src="doc/img/testing/manual/22.png" width="400px">
</details>

| Feature         | Action               | Expected Result                                           | Actual Result        |
|------------------|----------------------|------------------------------------------------------------|----------------------|
| Review Editing   | Edit/delete a review | Review updates or removal is processed correctly          | Works as expected    |



### Known Bugs
- (strictly not a bug) both datamodels "Product" and "Review" have a FloatField for Rating. Only Review should be used

---

## Deployment
### Key Migration Steps:

We migrated the project from Heroku to [Render.com](https://render.com). This change was driven by the deprecation of Heroku’s free tier and the need for more flexible infrastructure.

- Switched from Heroku to Render’s **Infrastructure-as-Code approach** 
- Recreated all necessary environment variables and secrets within the Render dashboard.
- Connected the Render web service to the GitHub repository with automatic deploys on push.
- Adjusted static file handling and build commands to match Render’s expectations.
   - finally, I needed to manually copy my static and media files to the s3 bucket of AWS 
- Verified that database migrations and management commands still execute correctly after deployment.
- Set up a **custom domain** and enabled **automatic SSL/TLS encryption** via Render’s built-in services.


#### Benefits of Render:

- No need for separate add-ons for SSL or cron jobs.
- Persistent free tier for small applications.
- Clear and fast deployment logs.
- Git-based CI/CD included by default.

---

## References and Credits

**Credits:** 



**References:** 

- Django docs
- Stripe docs
- Bootstrap 5.3 docs (what a powerful tool)
- Learning material from Code Institute 


**Media:**

- suit01.jpg by [Deepak Verma](https://www.pexels.com/@deepcreation/) on pexels.com
- suit02.jpg by [Pixabay](https://www.pexels.com/@pixabay/) on pexels.com
- suit03.jpg by [Tima Miroshnichenko](https://www.pexels.com/@tima-miroshnichenko/) on pexels.com
- suit04.jpg by [Antoni Shkraba](https://www.pexels.com/@shkrabaanthony/) Studio on pexels.com
- suit05.jpg by [Andrea Piacquadio](https://www.pexels.com/@olly/) on pexels.com
- suit06.jpg by [Lazarus Ziridis](https://www.pexels.com/@lazarus-ziridis-351891426/) on pexels.com
- suit07.jpg by [Tima Miroshnichenko](https://www.pexels.com/@tima-miroshnichenko/) on pexels.com
- suit08.jpg by [Tima Miroshnichenko](https://www.pexels.com/@tima-miroshnichenko/) on pexels.com
- suit09.jpg by [Antoni Shkraba](https://www.pexels.com/@shkrabaanthony/) Studio on pexels.com
- suit10.jpg by [Pavel Danilyuk](https://www.pexels.com/@pavel-danilyuk/) on pexels.com
- suit11.jpg by [Gustavo Fring](https://www.pexels.com/@gustavo-fring/) on pexels.com

All other images, such as gallery images for the shop, are generated with the AI-based online-tool [freepik.com](https://freepik.com)

---

## Acknowledgements

- Thanks Mo for your guidance (and patience)
