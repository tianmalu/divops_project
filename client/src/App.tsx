import "./App.css";
import { Routes, Route } from "react-router";

const App = () => {
  return (
    <Routes>
      <Route path="/" element={<App />} />
      <Route path="/login" element={<App />} />
      <Route path="/signup" element={<App />} />
      <Route path="/*" element={<h1>404 Page Not Found</h1>} />
    </Routes>
  );
};

export default App;
