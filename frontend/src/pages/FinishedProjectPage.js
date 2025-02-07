import React, { useState, useEffect } from "react";
import { Box, Modal } from "@mui/material";
import SwitchButton from "../components/SwitchButton";
import SingleSelector from "../components/SingleSelector";
import FinishedProjectContent from "../components/FinishedProjectContent";
import ProjectFeedback from "./ProjectFeedback";
import "../style/FinishedProjectPage.css";

const FinishedProjectPage = () => {
  const [sortOption, setSortOption] = useState("최신순");
  const [filterOption, setFilterOption] = useState("전체");
  const [showOnlyUnreviewed, setShowOnlyUnreviewed] = useState(false);
  const [displayedProjects, setDisplayedProjects] = useState([]);

  const [selectedProject, setSelectedProject] = useState(null); // 선택한 프로젝트 저장
  const [isFeedbackOpen, setIsFeedbackOpen] = useState(false); // 모달 상태 관리

  const [projects, setProjects] = useState([
    {
      projectID: 1,
      projectName: "기업-매칭 프리랜서 매칭 플랫폼 프론트엔드 개발",
      duration: 30,
      budget: 3000000,
      workType: 0, // 근무 형태(상주: 0, 원격: 1), 필터링에 사용할 속성
      // contractType: ,
      status: 0, // 진행 상태(시작 전: 0, 진행 중: 1, 완료: 2)
      registerDate: "20250113",
      categoryRole: "개발", // 직군
      categoryName: "소프트웨어/IT",
      // skillIdList: ,
      skillNameList: ["React", "TypeScript", "Next.js"],
      expertise: null, // 전문성
      proactiveness: null, // 적극성
      punctuality: null, // 일정준수
      maintainability: null, // 유지보수
      communication: null, // 의사소통
      feedbackContent: "",
      isReviewed: false, // 스위치에 사용할 속성
      locationName: "서울특별시 강남구",
    },
    {
      projectID: 2,
      projectName: "AI Chatbot Development",
      duration: 30,
      budget: 4000000,
      workType: 1, // 근무 형태(상주: 0, 원격: 1), 필터링에 사용할 속성
      status: 2, // 진행 상태(시작 전: 0, 진행 중: 1, 완료: 2)
      registerDate: "20241213",
      // endDate: "20250112",
      categoryRole: "개발",
      categoryName: "소프트웨어/IT", // 직군
      // skillIdList: ,
      skillNameList: ["Python", "Machine Learning", "Deep Learning"],
      expertise: null, // 전문성
      proactiveness: null, // 적극성
      punctuality: null, // 일정준수
      maintainability: null, // 유지보수
      communication: null, // 의사소통
      feedbackContent: "",
      isReviewed: false, // 스위치에 사용할 속성
      locationName: "서울특별시 서초구",
    },
  ]);

  // endDate 계산 함수
  const calculateEndDate = (registerDate, duration) => {
    const year = parseInt(registerDate.slice(0, 4), 10);
    const month = parseInt(registerDate.slice(4, 6), 10) - 1; // 월은 0부터 시작
    const day = parseInt(registerDate.slice(6, 8), 10);

    const startDate = new Date(year, month, day);
    startDate.setDate(startDate.getDate() + duration); // 종료일 계산

    const endYear = startDate.getFullYear();
    const endMonth = String(startDate.getMonth() + 1).padStart(2, "0");
    const endDay = String(startDate.getDate()).padStart(2, "0");

    return `${endYear}${endMonth}${endDay}`;
  };

  // 필터링 & 정렬 기능 적용
  useEffect(() => {
    let updatedProjects = projects.map((project) => ({
      ...project,
      endDate: calculateEndDate(project.registerDate, project.duration),
      radarData:
        project.expertise !== null
          ? [
              project.expertise,
              project.proactiveness,
              project.punctuality,
              project.maintainability,
              project.communication,
            ]
          : [],
    }));

    // 평가하지 않은 프로젝트만 보기 기능 적용
    if (showOnlyUnreviewed) {
      updatedProjects = updatedProjects.filter(
        (project) => !project.isReviewed
      );
    }

    // 필터링 적용 (근무 형태: 전체 / 상주(0) / 원격(1))
    if (filterOption !== "전체") {
      const mappedValue = Number(filterOption); // "0" → 0, "1" → 1 변환
      updatedProjects = updatedProjects.filter(
        (project) => project.workType === mappedValue
      );
    }

    // 정렬 적용 (최신순 / 금액 높은순)
    if (sortOption === "최신순") {
      updatedProjects.sort((a, b) =>
        b.registerDate.localeCompare(a.registerDate)
      );
    } else if (sortOption === "금액 높은순") {
      updatedProjects.sort((a, b) => Number(b.budget) - Number(a.budget));
    }

    setDisplayedProjects(updatedProjects);
  }, [sortOption, filterOption, showOnlyUnreviewed, projects]); // 옵션(정렬/필터/스위치) 변경 시 실행

  // 평가하기 버튼을 클릭 시 프로젝트의 isReviewed 상태를 변경하고 팝업 창 오픈
  const handleReview = (project) => {
    setSelectedProject(project);
    setIsFeedbackOpen(true); // 모달 열기
  };

  const handleFeedbackSubmit = (projectID, feedbackData) => {
    setProjects((prevProjects) =>
      prevProjects.map((project) =>
        project.projectID === projectID
          ? {
              ...project,
              ...feedbackData,
              isReviewed: true,
              feedbackScore:
                (feedbackData.expertise +
                  feedbackData.proactiveness +
                  feedbackData.punctuality +
                  feedbackData.maintainability +
                  feedbackData.communication) /
                5, // ✅ 평균 점수 계산
            }
          : project
      )
    );
    setIsFeedbackOpen(false); // 모달 닫기
  };

  return (
    <div className="finished-project-page-container">
      <div className="header-container">
        <h3 className="header">완료된 프로젝트</h3>
        <p>총 {displayedProjects.length}개의 완료된 프로젝트가 있습니다.</p>
      </div>
      <div className="filters">
        <div className="filter-group-left">
          {/* 필터용 SingleSelector */}
          <SingleSelector
            title="근무 형태"
            options={["전체", "상주", "원격"]}
            onChange={(value) => {
              const mapping = { 전체: "전체", 상주: "0", 원격: "1" }; // 숫자가 아닌 문자열로 저장
              setFilterOption(mapping[value]);
            }}
          />
        </div>
        <div className="filter-group-right">
          {/* SwitchButton을 클릭하면 setShowOnlyUnreviewed 값 변경 */}
          <SwitchButton
            text="평가하지 않은 프로젝트만 표시"
            onChange={setShowOnlyUnreviewed}
          />

          {/* 정렬용 SingleSelector */}
          <SingleSelector
            title="정렬 기준"
            options={["최신순", "금액 높은순"]}
            onChange={setSortOption}
          />
        </div>
      </div>

      {/* 필터링 + 정렬된 프로젝트 리스트 */}
      {displayedProjects.map((project) => (
        <FinishedProjectContent
          key={project.projectID}
          content={project}
          onReview={() => handleReview(project)}
        /> // 평가 버튼 클릭 시 호출
      ))}

      {/* 평가 모달 (기존 페이지 위에 오버레이) */}
      <Modal open={isFeedbackOpen} onClose={() => setIsFeedbackOpen(false)}>
        <Box
          sx={{
            position: "fixed",
            top: "50%",
            left: "50%",
            transform: "translate(-50%, -50%)",
            width: "80%",
            bgcolor: "white",
            p: 3,
            borderRadius: 2,
            boxShadow: 3,
          }}
        >
          {selectedProject && (
            <ProjectFeedback
              project={selectedProject}
              onClose={() => setIsFeedbackOpen(false)}
              onSubmit={handleFeedbackSubmit}
            />
          )}
        </Box>
      </Modal>
    </div>
  );
};

export default FinishedProjectPage;
