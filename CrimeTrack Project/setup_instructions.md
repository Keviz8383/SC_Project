# Setup Instructions - CrimeTrack

Follow these steps to get the CrimeTrack system running on your local machine.

## Prerequisites
- Python 3.8+
- Node.js (for potential frontend hosting, though not strictly required for simple viewing)
- A [Supabase](https://supabase.com/) Account
- A [Google Maps API Key](https://console.cloud.google.com/google/maps-apis)

---

## 1. Supabase Configuration
1. **Create a new project** in Supabase.
2. **Database Setup**:
   - Go to the **SQL Editor** in the Supabase Dashboard.
   - Copy and paste the contents of `supabase_schema.sql` (found in the root directory) and click **Run**.
3. **Storage Setup**:
   - Go to **Storage**.
   - Create a new bucket named `crime-evidence`.
   - Set the bucket to **Public**.
4. **API Keys**:
   - Go to **Project Settings > API**.
   - Copy the `Project URL`, `anon public key`, and `service_role key`.

---

## 2. Backend Setup
1. **Navigate to the backend directory**:
   ```bash
   cd backend
   ```
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Configure Environment Variables**:
   - Create a file named `.env` in the `backend/` folder.
   - Add the following:
     ```env
     SUPABASE_URL=your-project-url
     SUPABASE_KEY=your-anon-key
     SUPABASE_SERVICE_ROLE_KEY=your-service-key
     SECRET_KEY=your-random-secret-key
     DEBUG=True
     ```
4. **Run the Flask Server**:
   ```bash
   python -m app.main
   ```
   The API will start at `http://localhost:5000`.

---

## 3. Frontend Setup
1. **Configure Google Maps**:
   - Open `frontend/citizen.html`.
   - Replace `YOUR_GOOGLE_MAPS_API_KEY` in the script tag with your actual API key.
2. **Run the Frontend**:
   - Simply open `frontend/index.html` in your browser.
   - For a better experience, use a local server like Live Server (VS Code extension) or run:
     ```bash
     python -m http.server 8000
     ```
     Then navigate to `http://localhost:8000`.

---

## 4. Usage Guide
1. **Register** as a **Citizen** to report crimes.
2. **Register** as an **Administrator** (using the same email won't work, use a different one) to manage reports.
3. **Report a Crime**: Use the map to pick a location, fill the details, and upload images.
4. **Track**: Click on a complaint in your dashboard to see its history.
5. **Admin**: View charts and update statuses with remarks.

---

## Security Note
- In a production environment, ensure your `SECRET_KEY` is kept private.
- Set up proper **CORS** origins in `backend/app/main.py`.
- Apply **Row Level Security (RLS)** in Supabase as defined in the schema.
