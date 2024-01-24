import PageHeader from "../Components/PageHeader.jsx";
import SearchBar from "../Components/SearchBar.jsx";
import "./homepage.css";
export default function Homepage() {
  return (
    <>
      <PageHeader isLoggedIn={true} isAdmin={false} />
      <SearchBar />
    </>
  );
}
