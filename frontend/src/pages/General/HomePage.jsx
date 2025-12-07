/**
 * 
 */

  import { useNavigate } from "react-router-dom";

  import { Button } from "../../components/ui/Button";
  import unibenEngineeringImg from "../../assets/uniben_engineering.jpg";
  import bookShelvesImg from "../../assets/book_shelves.png";
  import studyIcon from "../../assets/study_colored_icon.png";
  import profileIcon from "../../assets/user_colored_icon.png";
  import searchIcon from "../../assets/search_colored_icon.png";
  import solutionIcon from "../../assets/book_open_thick_colored_icon.png";
  import reportIcon from "../../assets/report_colored_icon.png";
  import plusIcon from "../../assets/plus_icon.png";



export default function HomePage() {
  const navigate = useNavigate();
  const navigateToRegister = () => navigate("/register");
  const navigateToLogin = () => navigate("/login");
  
  return(
    <div className="w-100 h-screen bg-img-desktop bg-contain">
      {/* -------------------- HEADER -------------------- */}
      <header className="p-2 mb-10 flex justify-between items-center">
        <h3 className="text-primary-dark">UnibenEngVault</h3>
        <div className="flex gap-2 mr-10">
          <Button
            type="button"
            variant="outline"
            size="md"
            onClick={navigateToLogin}
            children="Login"
          />
          <Button
            type="button"
            variant="primary"
            size="md"
            onClick={navigateToRegister}
            children="Register"
          />
        </div>
      </header>

      {/* -------------------- MAIN -------------------- */}
      <main>
        {/* INTRODUCTION SECTION */}
        <section className="w-85 mb-8 mx-auto relative d-flex flex-row-reverse">
          <img 
            src={unibenEngineeringImg}
            alt="Uniben Engineering Faculty"
            className="w-100 max-w-26 h-23 rounded-br-20 shadow-primary-md-top hero-section"
            />
          <div
            className="max-w-24 max-h-22 p-5 bg-primary-light-50 absolute top-6 right-21"
          >
            <h2 className="text-primary-dark mb-1 hero-section">Welcome To UnibenEngVault</h2>
            <p className="leading-normal font-semibold">
              Uniben Engineering Vault (UnibenEngVault) is a centralized platform that
              hosts academic materials for all departments within the Faculty of Engineering.
              Students can freely search for and stream resources online. However, full access to
              download or view complete content is restricted to registered users with an active account.
              Registration is free.
            </p>
          </div>
        </section>

        {/* MORE INTRO SECTION */}
          <section className="w-95p mb-15 mx-auto relative d-flex flex-row-reverse">
            <img
              src={bookShelvesImg}
              alt="Book Shelves"
              className="w-100 h-19 mt-6"
            />
            <div
            className="leading-normal font-semibold max-w-24 h-20 px-5 py-9 bg-primary-light-50 absolute top-1 right-15"
            >
              This digital library is exclusively designed for undergraduate students in the Faculty of Engineering
              at the University of Benin. It serves as a dedicated academic space to support learning, revision and
              collaboration among engineering students.
            </div>
          </section>

        {/* INFOMATION SECTION */}
          <section className="w-85 mb-15 mx-auto">
            <h5 className="text-primary-dark text-center mb-15">Gain Easy Access To Courses Within the Faculty</h5>
            
            <div className="grid grid-cols-3 row-gap-10">
            <div className="flex flex-col items-center">
              <img
                src={studyIcon}
                alt="Study"
                className="max-w-11 mb-5 bg-white p-2 border-primary rounded-br-10 shadow-primary-t-icon"
              />
              <h5 className="text-primary-dark mb-1">Study</h5>
              <p className="px-7">
                Only engineering courses offered in the Faculty of 
                Engineering and your department will be available.
              </p>
            </div>

            <div className="flex flex-col items-center">
              <img
                src={profileIcon}
                alt="Profile"
                className="max-w-11 mb-5 bg-white p-2 border-primary rounded-br-10 shadow-primary-t-icon"
              />
              <h5 className="text-primary-dark mb-1">Profile</h5>
              <p className="px-7">
                Access a personalized dashboard that display courses
                based on the information provided in your profile.
              </p>
            </div>

            <div className="flex flex-col items-center">
              <img
                src={searchIcon}
                alt="search"
                className="max-w-11 mb-5 bg-white p-2 border-primary rounded-br-10 shadow-primary-t-icon"
              />
              <h5 className="text-primary-dark mb-1">Search</h5>
              <p className="px-7">
                Easily search for courses by course code or level
                to quickly find materials that match your academic needs.
              </p>
            </div>

            <div className="flex flex-col items-center">
              <img
                src={solutionIcon}
                alt="solution"
                className="max-w-11 mb-5 bg-white p-2 border-primary rounded-br-10 shadow-primary-t-icon"
              />
              <h5 className="text-primary-dark mb-1">Solutions</h5>
              <p className="px-7">
                Easily upload study materials for others to access, and browse
                solutions to past exam questions from your department.
              </p>
            </div>

            <div className="flex flex-col items-center">
              <img
                src={reportIcon}
                alt="report"
                className="max-w-11 mb-5 bg-white p-2 border-primary rounded-br-10 shadow-primary-t-icon"
              />
              <h5 className="text-primary-dark mb-1">Report</h5>
              <p className="px-7">
                Report incorrect or outdated materials, and request specific course
                materials that are currently  unavailable on the platform.
              </p>
            </div>
            </div>
          </section>

        {/* STATS SECTION */}
          <section className="w-95p mb-14 text-white py-5 px-12 p bg-primary flex justify-around items-center">
            <div className="w-25 flex items-center">
              <p></p>
              <p>DEPARTMENTS IN THE FACULTY OF ENGINEERING</p>
            </div>

            <div className="w-25 flex items-center">
              <p></p>
              <img 
              src={plusIcon}
              alt="plus"
              className="max-w-5"
              />
            <p>REGISTERED ENGINEERING STUDENTS</p>
          </div>

          <div className="w-25 flex justify-between items-center">
            <p></p>
            <img 
              src={plusIcon}
              alt="plus"
              className="max-w-5"
              />
            <p>UPLOADED COURSE MATERIALS AND PAST QUESTIONS</p>
          </div>
        </section>

        {/* CTA SECTION */}
          <section className="w-50 mb-18 mx-auto flex justify-center items-center">
            <Button
              type="button"
              variant="secondary"
              size="lg"
              onClick={navigateToRegister}
              children="START STUDYING NOW"
            />
          </section>
        </main>

      {/* -------------------- FOOTER -------------------- */}
      <footer className="w-85 mb-8 mx-auto flex justify-between">
        <div>
          <p className="mb-2 text-primary-dark font-semibold">Content</p>
          <ul className="flex flex-col gap-1">
            <li>All Courses</li>
            <li>Past Exam Questions</li>
            <li>Solution to Past Questions</li>
            <li>Course Outline</li>
          </ul>
        </div>

        <div>
          <p className="text-primary-dark font-semibold">Information</p>
          <ul className="">
            <li>Study</li>
            <li>Admin</li>
            <li>About Us</li>
            <li>Place Adverts</li>
          </ul>
        </div>

        <div>
          <p className="text-primary-dark font-semibold">Legal</p>
          <ul className="">
            <li>Cookies Settings</li>
            <li>Terms and Conditions</li>
            <li>cookies Policy</li>
            <li>Copyright Information</li>
          </ul>
        </div>

        <div>
          <p className="text-primary-dark font-semibold">Support</p>
          <ul className="">
            <li>Sponsors</li>
            <li>FAQ</li>
          </ul>
        </div>
      </footer>
    </div>
  );
} 

