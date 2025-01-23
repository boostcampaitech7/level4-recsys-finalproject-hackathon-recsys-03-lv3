import React, { useState, useEffect, forwardRef } from "react";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import "../style/chat.css";

const teams = [
  "front-end developer",
  "back-end developer",
  "ai developer",
  "data scientist",
  "designer",
  "project manager",
  "graphics developer",
  "system administrator",
  "mobile developer",
  "full-stack developer",
  "qa developer",
  "embedded applications developer",
  "data analyst",
  "data engineer",
  "hardware engineer",
  "cloud infrastructure engineer",
  "devops",
  "r&d",
  "blockchain",
  "security",
  "site reliability engineer",
];

const Chat = () => {
  const [chatHistory, setChatHistory] = useState([]);
  const [selectedTeams, setSelectedTeams] = useState([]);
  const [userInput, setUserInput] = useState("");
  const [step, setStep] = useState(0);
  const [isTeamButtonClicked, setIsTeamButtonClicked] = useState(false);
  const [isDeadlineButtonClicked, setIsDeadlineButtonClicked] = useState(false);
  const [isClearable, setIsClearable] = useState(true);
  const [projectData, setProjectData] = useState({
    team: "",
    title: "",
    content: "",
    period: "",
  });
  const [dateRange, setDateRange] = useState([null, null]);
  const [startDate, endDate] = dateRange;

  const questions = [
    "요청할 부서를 선택해주세요.",
    "요청할 프로젝트의 제목을 입력해주세요.",
    "요청할 프로젝트의 마감기한을 선택해주세요.",
    "요청할 프로젝트의 내용을 입력해주세요.",
  ];

  // 첫 번째 질문 표시
  useEffect(() => {
    setChatHistory([{ sender: "bot", text: questions[0] }]);
  }, []);

  const getSelectedTeamsText = () => {
    if (selectedTeams.length === 0) {
      return "# New Chat";
    } else if (selectedTeams.length === 1) {
      return `# ` + selectedTeams[0];
    } else {
      return `# ${selectedTeams[0]} 외 ${selectedTeams.length - 1}팀`;
    }
  };

  const handleTeamChange = (team) => {
    setSelectedTeams(
      (prev) =>
        prev.includes(team)
          ? prev.filter((item) => item !== team) // 이미 선택된 부서는 제거
          : [...prev, team] // 선택되지 않은 부서는 추가
    );
  };

  const handleUserInput = () => {
    let updatedChat = [...chatHistory];
    if (step === 0) {
      setProjectData({ ...projectData, team: selectedTeams.join(", ") });
      setIsTeamButtonClicked(true);
    } else if (step === 1) {
      updatedChat.push({ sender: "user", text: userInput });
      setProjectData({ ...projectData, title: userInput });
    } else if (step === 2) {
      const period = `${startDate?.toLocaleDateString("ko-KR")} ~ ${endDate?.toLocaleDateString(
        "ko-KR"
      )}`;
      setProjectData({ ...projectData, period });
      setIsDeadlineButtonClicked(true);
      setIsClearable(false);
    } else if (step === 3) {
      updatedChat.push({ sender: "user", text: userInput });
      setProjectData({ ...projectData, content: userInput });

      updatedChat.push({
        sender: "bot",
        text: (
          <div className="project-overview">
            <p className="fw-bold mb-3">
              요청할 프로젝트의 전체적인 개요를 확인해주세요.
            </p>
            <table className="table table-bordered">
              <tbody>
                <tr>
                  <th>프로젝트 이름</th>
                  <td>{projectData.title || "프로젝트 이름 없음"}</td>
                </tr>
                <tr>
                  <th>프로젝트 기간</th>
                  <td>{projectData.period || "날짜 선택 안 됨"}</td>
                </tr>
                <tr>
                  <th>담당 부서</th>
                  <td>{projectData.team || "부서 선택 안 됨"}</td>
                </tr>
                <tr>
                  <th>기술 요구사항</th>
                  <td>
                    <span className="badge bg-light text-dark border border-dark rounded m-2 px-3 py-2 fw-normal fs-6">
                      Python
                    </span>
                    <span className="badge bg-light text-dark border border-dark rounded m-2 px-3 py-2 fw-normal fs-6">
                      TensorFlow
                    </span>
                    <span className="badge bg-light text-dark border border-dark rounded m-2 px-3 py-2 fw-normal fs-6">
                      Pandas
                    </span>
                  </td>
                </tr>
                <tr>
                  <th>프로젝트 내용</th>
                  {/* {userInput || "내용 없음"} */}
                  <td>
                    <ul>
                      <li>
                        <strong>Task 1:</strong> 데이터 수집 및 전처리
                        (Python_Data Analysis_API)
                        <ul>
                          <li>
                            고객 리뷰 데이터를 수집하고 전처리하여 분석에 적합한
                            형태로 변환
                          </li>
                          <li>불필요한 정보 제거 및 정제</li>
                        </ul>
                      </li>
                      <li>
                        <strong>Task 2:</strong> 가상 분석 모델 개발
                        (NLP_Hugging Face_Transfer Learning)
                        <ul>
                          <li>
                            Hugging Face의 사전 훈련된 모델을 활용하여 고객
                            리뷰의 감정 분석
                          </li>
                          <li>필요에 따라 모델 미세 조정</li>
                        </ul>
                      </li>
                      <li>
                        <strong>Task 3:</strong> 키워드 추출 및 텍스트 분석
                        (NLP_Text Mining_Data Visualization)
                        <ul>
                          <li>주요 키워드 추출, 트렌드 분석, 시각화</li>
                        </ul>
                      </li>
                    </ul>
                  </td>
                </tr>
              </tbody>
            </table>
            <div className="d-flex">
              <button
                className="btn btn-link ms-auto"
                type="button"
                id="sendRequest"
                onClick={() => {
                  alert("요청이 완료되었습니다.");
                  window.location.reload(); //window.location.href = "https://example.com";
                }}
              >
                <i class="fa-solid fa-arrow-right me-2 fw-bold"></i>
                요청 보내기
              </button>
            </div>
          </div>
        ),
      });
    }

    // 다음 질문 추가
    if (step < questions.length - 1 && step !== 3) {
      updatedChat.push({ sender: "bot", text: questions[step + 1] });
    }

    setChatHistory(updatedChat);
    setStep((prev) => prev + 1);
    setUserInput(""); // 입력 초기화
  };

  const CustomInput = forwardRef(({ value, onClick }, ref) => (
    <div
      className="custom-date-picker-input d-flex align-items-center px-4 py-2 border rounded"
      onClick={onClick}
      ref={ref}
      style={{
        backgroundColor: "#f8f9fa",
        cursor: "pointer",
        width: "100%",
        justifyContent: "space-between",
      }}
    >
      <span className="px-3 me-3">{value || "YYYY.MM.DD ~ YYYY.MM.DD"}</span>
      <i className="fa-regular fa-calendar-days"></i>
    </div>
  ));

  return (
    <div className="chat-page d-flex flex-column">
      {/* Header */}
      <div className="chat-header rounded-top d-flex align-items-center justify-content-between bg-primary bg-gradient text-white p-3 border-bottom">
        <h4 className="m-0">{getSelectedTeamsText()}</h4>
      </div>

      {/* Chat Body */}
      <div
        className="chat-body bg-primary-subtle flex-grow-1 p-2"
        style={{ overflowY: "auto", backgroundColor: "#f8f9fa" }}
      >
        {chatHistory.map((chat, idx) => (
          <div
            key={idx}
            className={`chat-bubble d-flex ${
              chat.sender === "user"
                ? "justify-content-end mb-3"
                : "align-items-start mb-3"
            }`}
          >
            {/* 챗봇 메시지에만 아이콘 추가 */}
            {chat.sender === "bot" && (
              <div className="chat-icon bg-primary text-white rounded-circle d-flex align-items-center justify-content-center m-2">
                <i className="fas fa-user"></i>
              </div>
            )}
            <div
              className={`chat-content ${
                chat.sender === "user" ? "bg-primary text-white" : "bg-white"
              } p-3 rounded shadow-sm`}
            >
              {chat.text === questions[0] ? (
                <div>
                  <p className="m-1 mb-2">{chat.text}</p>
                  <div className="d-flex align-items-center">
                    <div className="dropdown me-2 w-100">
                      <button
                        className="btn btn-light dropdown-toggle w-100 d-flex justify-content-between align-items-center"
                        type="button"
                        id="dropdownMenuButton"
                        data-bs-toggle="dropdown"
                        aria-expanded="false"
                      >
                        {selectedTeams.length > 0
                          ? `${selectedTeams.length} Teams Selected`
                          : "Teams"}
                      </button>
                      <ul
                        className="dropdown-menu"
                        aria-labelledby="dropdownMenuButton"
                      >
                        {teams.map((team) => (
                          <li key={team} className="dropdown-item">
                            <label>
                              <input
                                type="checkbox"
                                value={team}
                                checked={selectedTeams.includes(team)}
                                onChange={() => handleTeamChange(team)}
                              />
                              {" " + team}
                            </label>
                          </li>
                        ))}
                      </ul>
                    </div>
                    <button
                      className={`btn ${
                        isTeamButtonClicked ? "btn-secondary" : "btn-primary"
                      }`}
                      onClick={handleUserInput}
                      disabled={
                        selectedTeams.length === 0 || isTeamButtonClicked
                      }
                    >
                      ✓
                    </button>
                  </div>
                </div>
              ) : chat.text === questions[2] ? (
                <div>
                  <p className="m-1 mb-2">{chat.text}</p>
                  <div className="d-flex align-items-center">
                    <DatePicker
                      selected={startDate}
                      onChange={(update) => setDateRange(update)}
                      startDate={startDate}
                      endDate={endDate}
                      selectsRange
                      dateFormat="yyyy.MM.dd"
                      isClearable={isClearable}
                      customInput={<CustomInput />}
                      className="me-2"
                    />
                    <button
                      className={`btn ${
                        isDeadlineButtonClicked
                          ? "btn-secondary"
                          : "btn-primary"
                      } ms-2`}
                      onClick={() => {
                        if (startDate && endDate) {
                          handleUserInput();
                          setIsDeadlineButtonClicked(true); // 마감기한 버튼 클릭 처리
                          setIsClearable(false);
                        }
                      }}
                      disabled={
                        !startDate || !endDate || isDeadlineButtonClicked
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
      <div className="chat-input d-flex align-items-center p-3 border bg-white">
        <input
          type="text"
          className="form-control mr-2"
          placeholder="메시지를 입력하세요..."
          value={userInput}
          onChange={(e) => setUserInput(e.target.value)}
          disabled={step >= questions.length}
        />
        <button
          className="btn btn-primary"
          onClick={handleUserInput}
          disabled={step >= questions.length}
        >
          <i
            class="fa-regular fa-paper-plane"
            style={{ transform: "scaleX(-1)", display: "inline-block" }}
          ></i>
        </button>
      </div>
    </div>
  );
};

export default Chat;
