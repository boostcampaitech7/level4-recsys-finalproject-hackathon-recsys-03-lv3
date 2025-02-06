import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import "react-datepicker/dist/react-datepicker.css";
import "../style/ProjectInputPage.css";
import ProfileIcon from "../components/ProfileIcon";
import botphoto from "../assets/chat_logo.png";

const WorkMode = ["상주", "원격"];
const ProjectType = ["외주", "기간제"];
const Priority = ["스킬", "금액", "상관없음"];

const questions = [
  "요청할 프로젝트의 내용을 입력해주세요.",
  "요청할 프로젝트의 예상 기간을 입력해주세요.",
  "원하는 근무 형태를 선택해주세요.",
  "원하는 계약 유형을 선택해주세요.",
  "계약 시 우선순위 고려 대상을 선택해주세요.",
  "요청할 프로젝트의 예상 금액을 입력해주세요.",
];

const DropdownSelector = ({
  label,
  options,
  selectedValue,
  setSelectedValue,
  isButtonClicked,
  setIsButtonClicked,
  handleNextStep,
  dropdownIdx,
}) => {
  const DropdownList = ["근무 형태", "계약 유형", "우선순위"];

  return (
    <div className="content-box">
      <p className="chat-label">{label}</p>
      <div className="dropdown-container">
        <select
          className="custom-select"
          value={selectedValue}
          onChange={(e) => setSelectedValue(e.target.value)}
        >
          <option value="" disabled>
            {DropdownList[dropdownIdx]}
          </option>
          {options.map((option, index) => (
            <option key={index} value={option}>
              {option}
            </option>
          ))}
        </select>
        <button
          className={`custom-btn ${isButtonClicked ? "btn-disabled" : "btn-active"}`}
          onClick={() => {
            if (selectedValue) {
              handleNextStep();
              setIsButtonClicked(true);
            }
          }}
          disabled={!selectedValue || isButtonClicked}
        >
          ✓
        </button>
      </div>
    </div>
  );
};

const ProjectInputPage = () => {
  const navigate = useNavigate();

  const [chatHistory, setChatHistory] = useState([]);
  const [step, setStep] = useState(0);
  const [userInput, setUserInput] = useState("");
  const [selectedDuration, setSelectedDuration] = useState("");
  const [isDayButtonClicked, setDayIsButtonClicked] = useState(false);
  const [selectedWorkMode, setSelectedWorkMode] = useState("");
  const [isWorkModeButtonClicked, setIsWorkModeButtonClicked] = useState(false);
  const [selectedProjectType, setSelectedProjectType] = useState("");
  const [isProjectTypeButtonClicked, setIsProjectTypeButtonClicked] =
    useState(false);
  const [selectedPriority, setSelectedPriority] = useState("");
  const [isPriorityButtonClicked, setIsPriorityButtonClicked] = useState(false);
  const [selectedContractType, setSelectedContractType] = useState("월");
  const [selectedBudget, setSelectedBudget] = useState("");
  const [isBudgetButtonClicked, setIsBudgetButtonClicked] = useState(false);
  const [projectData, setProjectData] = useState({
    projectContent: "",
    duration: "",
    workMode: "",
    projectType: "",
    priority: "",
    contrastType: "",
    budget: "",
  });

  // 첫 번째 질문 표시
  useEffect(() => {
    setChatHistory([{ sender: "bot", text: questions[0] }]);
  }, []);

  const handleUserInput = () => {
    let updatedChat = [...chatHistory];

    if (step === 0) {
      updatedChat.push({ sender: "user", text: userInput });
      setProjectData((prev) => ({
        ...prev,
        projectContent: userInput,
      }));
    } else if (step === 1) {
      setProjectData((prev) => ({
        ...prev,
        duration: selectedDuration,
      }));
    } else if (step === 2) {
      setProjectData((prev) => ({
        ...prev,
        workMode: selectedWorkMode,
      }));
    } else if (step === 3) {
      setProjectData((prev) => ({
        ...prev,
        projectType: selectedProjectType,
      }));
    } else if (step === 4) {
      setProjectData((prev) => ({
        ...prev,
        priority: selectedPriority,
      }));
    } else if (step === 5) {
      setProjectData((prev) => ({
        ...prev,
        contrastType: selectedContractType,
        budget: selectedBudget,
      }));
    }

    if (step === questions.length - 1) {
      updatedChat.push({ sender: "bot", text: "요약 중..." });
      setChatHistory(updatedChat);

      setTimeout(() => {
        navigate("/register-result", { state: { projectData } });
      }, 2000);
    } else {
      updatedChat.push({ sender: "bot", text: questions[step + 1] });
    }

    setChatHistory(updatedChat);
    setStep((prev) => prev + 1);
    setUserInput(""); // 입력 초기화
  };

  return (
    <div className="chat-page">
      {/* Header */}
      <div className="chat-header">
        <span>새 프로젝트 등록</span>
      </div>

      {/* Chat Body */}
      <div className="chat-body">
        {chatHistory.map((chat, idx) => (
          <div
            key={idx}
            className={`chat-bubble ${chat.sender === "user" ? "user" : "bot"}`}
          >
            {/* 챗봇 메시지에만 아이콘 추가 */}
            {chat.sender === "bot" && (
              <div className="chat-icon m-2">
                <ProfileIcon
                  profileImage={botphoto}
                  style={{
                    width: "45px",
                    height: "47px",
                    margin: "0",
                  }}
                />
              </div>
            )}
            <div className={`chat-content ${chat.sender}`}>
              {chat.text === questions[1] ? (
                // Duration
                <div className="content-box">
                  <p className="chat-label">{chat.text}</p>
                  <div className="custom-input-container">
                    <input
                      className="custom-input"
                      type="number"
                      value={selectedDuration}
                      onChange={(e) => setSelectedDuration(e.target.value)}
                      min="1"
                    />
                    <span className="unit-text">일</span>
                    <button
                      className={`custom-btn ${
                        isDayButtonClicked ? "btn-disabled" : "btn-active"
                      }`}
                      onClick={() => {
                        if (selectedDuration) {
                          handleUserInput();
                          setDayIsButtonClicked(true);
                        }
                      }}
                      disabled={
                        !selectedDuration ||
                        isNaN(selectedDuration) ||
                        isDayButtonClicked
                      }
                    >
                      ✓
                    </button>
                  </div>
                </div>
              ) : chat.text === questions[2] ? (
                // WorkMode
                <DropdownSelector
                  label={chat.text}
                  options={WorkMode}
                  selectedValue={selectedWorkMode}
                  setSelectedValue={(value) => {
                    setSelectedWorkMode(value);
                    setProjectData((prev) => ({
                      ...prev,
                      workMode: value,
                    }));
                  }}
                  isButtonClicked={isWorkModeButtonClicked}
                  setIsButtonClicked={setIsWorkModeButtonClicked}
                  handleNextStep={handleUserInput}
                  dropdownIdx={0}
                />
              ) : chat.text === questions[3] ? (
                // ProjectType
                <DropdownSelector
                  label={chat.text}
                  options={ProjectType}
                  selectedValue={selectedProjectType}
                  setSelectedValue={setSelectedProjectType}
                  isButtonClicked={isProjectTypeButtonClicked}
                  setIsButtonClicked={setIsProjectTypeButtonClicked}
                  handleNextStep={handleUserInput}
                  dropdownIdx={1}
                />
              ) : chat.text === questions[4] ? (
                // Priority
                <DropdownSelector
                  label={chat.text}
                  options={Priority}
                  selectedValue={selectedPriority}
                  setSelectedValue={setSelectedPriority}
                  isButtonClicked={isPriorityButtonClicked}
                  setIsButtonClicked={setIsPriorityButtonClicked}
                  handleNextStep={handleUserInput}
                  dropdownIdx={2}
                />
              ) : chat.text === questions[5] ? (
                // Budget
                <div className="content-box">
                  <p className="chat-label">{chat.text}</p>
                  <div className="budget-container">
                    <button
                      className="custom-btn btn-outline"
                      onClick={() =>
                        setSelectedContractType((prev) =>
                          prev === "월" ? "프로젝트" : "월"
                        )
                      }
                    >
                      {selectedContractType} 단위
                    </button>
                    <input
                      type="number"
                      className="custom-input"
                      placeholder={`${selectedContractType} 금액`}
                      value={selectedBudget}
                      onChange={(e) => setSelectedBudget(e.target.value)}
                    />
                    <span className="unit-text">원</span>
                    <button
                      className={`custom-btn ${isBudgetButtonClicked ? "btn-disabled" : "btn-active"}`}
                      onClick={() => {
                        if (selectedBudget) {
                          handleUserInput();
                          setIsBudgetButtonClicked(true);
                        }
                      }}
                      disabled={
                        !selectedBudget ||
                        isNaN(selectedBudget) ||
                        !selectedContractType ||
                        isBudgetButtonClicked
                      }
                    >
                      ✓
                    </button>
                  </div>
                </div>
              ) : typeof chat.text === "string" ? (
                chat.text.split("\n").map((line, i) => (
                  <p key={i} className="m-0">
                    {line}
                  </p>
                ))
              ) : (
                chat.text
              )}
            </div>
          </div>
        ))}
      </div>

      {/* Input Field */}
      <div className="chat-input">
        <input
          type="text"
          placeholder="메시지를 입력하세요..."
          value={userInput}
          onChange={(e) => setUserInput(e.target.value)}
          disabled={step >= questions.length}
        />
        <button
          className="custom-btn btn-send"
          onClick={handleUserInput}
          disabled={step >= questions.length}
        >
          <i class="fa-regular fa-paper-plane"></i>
        </button>
      </div>
    </div>
  );
};

export default ProjectInputPage;
