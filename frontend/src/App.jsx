import { BrowserRouter, Routes, Route, Link } from "react-router-dom";
import UploadPage from "./pages/UploadPage";
import SearchPage from "./pages/SearchPage";

export default function App() {
  return (
    <BrowserRouter>
      <nav style={{ display: "flex", gap: 12, padding: 12 }}>
        {/* <Link to="/">Upload</Link>  */}
        {/*   <Link to="/search">Search</Link>   */}
      </nav>
      <Routes>
       {/* <Route path="/" element={<UploadPage />} />  */}
        <Route path="/search" element={<SearchPage />} />
      </Routes>
    </BrowserRouter>
  );
}
