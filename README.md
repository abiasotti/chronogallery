# Chronogallery

**Version:** 0.1.3

Chronogallery is a Django-based web application for storing, organizing, and viewing photo albums. The platform features a modern, mobile-friendly interface with in-page modals, intuitive navigation, and seamless fullscreen photo browsing.

## Features (Implemented)

### Core Functionality
- **Photo Management:** Upload photos to albums with automatic cover assignment
- **Album Organization:** Create, edit, and delete albums with custom names and descriptions
- **Gallery Views:** Browse all photos in a grid layout or view albums individually
- **Photo Detail:** View full-size images with navigation between photos

### User Interface
- **Responsive Design:** Mobile-friendly layout with sidebar navigation
- **Modal Interactions:** In-page modals for uploads, editing, and confirmations
- **Drag-and-drop Upload:** Upload photos by dragging files onto the main gallery or directly onto an album page
- **Hamburger Menus:** Context-aware menus for albums, photos, and gallery pages
- **Navigation:** Previous/Next photo navigation in both regular and fullscreen views
- **Seamless Fullscreen Navigation:** AJAX-powered Previous/Next navigation in fullscreen mode for a true slideshow experience
- **Bulk Actions:** Select and delete multiple photos from the gallery

### Album Features
- **Album Creation:** Create new albums via modal form
- **Album Editing:** Modify album names and set custom covers
- **Album Deletion:** Safe deletion with confirmation modals
- **Cover Management:** Automatic cover assignment or manual selection

### Photo Features
- **Photo Upload:** Upload to specific albums or create new albums during upload (via modal or drag-and-drop)
- **Drag-and-drop Upload:** Drag files onto the main gallery (choose or create album) or onto an album page (direct upload)
- **Photo Actions:** Set as album cover, download, or delete photos
- **Photo Navigation:** Browse through photos chronologically, with seamless AJAX navigation in fullscreen
- **Bulk Delete:** Select and delete multiple photos from the main gallery

### Photo Selection & Bulk Actions
- **Modern Selection UI:** Select photos using a subtle circle overlay in the top-left of each thumbnail (visible on hover/always on mobile)
- **Bulk Actions in All Views:** Select, deselect, and delete multiple photos from both the main gallery and individual album views
- **Hamburger Menu Integration:** Access 'Select All' and 'Delete Selected' options from the hamburger menu in both gallery and album pages

## Project Structure
```
chronogallery/
├── chronogallery/          # Django project settings
├── gallery/               # Main Django app
│   ├── models.py         # Album and Photo models
│   ├── views.py          # Views for all pages and actions
│   ├── urls.py           # URL routing
│   └── templates/        # HTML templates
├── media/                # User-uploaded files (photos, covers)
├── manage.py            # Django management script
├── requirements.txt     # Python dependencies
├── Dockerfile          # Container configuration
└── .dockerignore       # Docker build exclusions
```

## Getting Started

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- (Recommended) Virtual environment tool (e.g., `venv` or `virtualenv`)

### Local Development Setup
1. **Clone the repository:**
   ```bash
   git clone <repo-url>
   cd chronogallery
   ```
2. **Create and activate a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Run migrations:**
   ```bash
   python manage.py migrate
   ```
5. **Start the development server:**
   ```bash
   python manage.py runserver
   ```
6. **Access the app:**
   Open your browser and go to [http://localhost:8000/](http://localhost:8000/)

### Docker Setup
1. **Build the image:**
   ```bash
   docker build -t chronogallery .
   ```
2. **Run the container:**
   ```bash
   docker run -p 8000:8000 -v $(pwd)/media:/app/media chronogallery
   ```

## Usage

### Navigation
- **Home:** View all photos in a grid layout
- **Albums:** Browse and manage albums
- **Upload:** Upload photos to albums via modals on the home or album pages

### Album Management
- **Create Album:** Use the hamburger menu on the albums page
- **Edit Album:** Click the hamburger menu on any album detail page
- **Delete Album:** Available in the edit modal with confirmation

### Photo Management
- **Upload Photos:** Use the upload modal on the home or album pages, or drag and drop files onto the main gallery (choose/create album) or onto an album page (direct upload)
- **View Photos:** Click any thumbnail to view full-size
- **Photo Actions:** Use the hamburger menu on photo detail pages
- **Navigate Photos:** Use Previous/Next buttons below the image (regular view) or seamless AJAX navigation in fullscreen
- **Bulk Delete:** Select and delete multiple photos from the main gallery or any album using the selection circles and hamburger menu

## Development Notes
- Uses SQLite database for development
- Media files are served in development mode
- Static files are collected for production
- All modals use vanilla JavaScript for simplicity
- Fullscreen navigation uses the browser Fullscreen API and AJAX for seamless experience

## Future Features
- [ ] Thumbnail generation for better performance
- [ ] Slideshow mode for albums
- [ ] User authentication and private albums
- [ ] Photo tagging and search
- [ ] Album sharing functionality
- [ ] Advanced image editing features

## Contributing
- Follow Django best practices
- Keep code modular and well-documented
- Test new features thoroughly
- Update this README for significant changes

## License
TBD

---

*This README will be updated as the project evolves. Feel free to add notes, todos, or architectural decisions here as we build Chronogallery.* 