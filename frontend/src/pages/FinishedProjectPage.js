import React, { useState, useEffect } from "react";
import SwitchButton from "../components/SwitchButton";
import SingleSelector from "../components/SingleSelector";
import FinishedProjectContent from "../components/FinishedProjectContent";
import "../style/FinishedProjectPage.css";

const FinishedProjectPage = () => {
  const [sortOption, setSortOption] = useState("최신순");
  const [filterOption, setFilterOption] = useState("전체");
  const [showOnlyUnreviewed, setShowOnlyUnreviewed] = useState(false);
  const [displayedProjects, setDisplayedProjects] = useState([]);

  const [projects, setProjects] = useState([
    {
      projectID: 1,
      projectName: "기업-매칭 프리랜서 매칭 플랫폼 프론트엔드 개발",
      duration: 30,
      registerDate: "20250113",
      endDate: "20250212",
      budget: 3000000,
      categoryName: "개발",
      role: "프론트엔드 개발자",
      workType: "원격", // 필터링에 사용할 속성
      skillNameList: ["React", "TypeScript", "Next.js"],
      isReviewed: false, // 스위치에 사용할 속성
      expertise: 5,
      proactiveness: 4,
      punctuality: 3,
      maintainability: 2,
      communication: 1,
      feedbackContent: "일정 내 원하는대로 구현해주셔서 감사합니다.",
    },
    {
      projectID: 2,
      projectName: "AI Chatbot Development",
      duration: 30,
      registerDate: "20241213",
      endDate: "20250112",
      budget: 4000000,
      categoryName: "개발",
      role: "AI 개발자",
      workType: "상주", // 필터링에 사용할 속성
      skillNameList: ["Python", "Machine Learning", "Deep Learning"],
      isReviewed: false, // 스위치에 사용할 속성
      expertise: 4.5,
      proactiveness: 4.0,
      punctuality: 4.2,
      maintainability: 4.0,
      communication: 4.3,
      feedbackContent: "일정 내 원하는대로 구현해주셔서 감사합니다.",
    },
  ]);

  projects.forEach((project) => {
    const {
      expertise,
      proactiveness,
      punctuality,
      maintainability,
      communication,
    } = project;
    project.feedbackScore =
      (expertise +
        proactiveness +
        punctuality +
        maintainability +
        communication) /
      5;
    project.radarData = [
      expertise,
      proactiveness,
      punctuality,
      maintainability,
      communication,
    ];
  });

  // 평가하기 버튼을 클릭하면 프로젝트의 isReviewed 상태를 변경
  const handleReview = (projectID) => {
    setProjects((prevProjects) =>
      prevProjects.map((project) =>
        project.projectID === projectID
          ? { ...project, isReviewed: true }
          : project
      )
    );
  };

  // 필터링 & 정렬 기능 적용
  useEffect(() => {
    let updatedProjects = [...projects];

    // 평가하지 않은 프로젝트만 보기 기능 적용
    if (showOnlyUnreviewed) {
      updatedProjects = updatedProjects.filter(
        (project) => !project.isReviewed
      );
    }

    // 필터링 적용 (전체 / 상주 / 원격)
    if (filterOption !== "전체") {
      updatedProjects = updatedProjects.filter(
        (project) => project.workType === filterOption
      );
    }

    // 정렬 적용 (최신순 / 추천순 / 금액 많은순)
    if (sortOption === "최신순") {
      updatedProjects.sort((a, b) =>
        b.registerDate.localeCompare(a.registerDate)
      );
    } else if (sortOption === "추천순") {
      updatedProjects.sort((a, b) => b.feedbackScore - a.feedbackScore);
    } else if (sortOption === "금액 많은순") {
      updatedProjects.sort((a, b) => b.budget - a.budget);
    }

    setDisplayedProjects(updatedProjects);
  }, [sortOption, filterOption, showOnlyUnreviewed, projects]); // 옵션(정렬/필터/스위치) 변경 시 실행

  return (
    <div className="finished-project-page-container">
      <div className="header-container">
        <div className="header-left">
          <h3 className="header">완료된 프로젝트</h3>
          <p>총 {projects.length}개의 완료된 프로젝트가 있습니다.</p>
        </div>

        <div className="header-right">
          {/* SwitchButton을 클릭하면 setShowOnlyUnreviewed 값 변경 */}
          <SwitchButton
            text="평가하지 않은 프로젝트만 표시"
            onChange={setShowOnlyUnreviewed}
          />

          {/* 정렬용 SingleSelector */}
          <SingleSelector
            title="정렬 기준"
            options={["최신순", "추천순", "금액 많은순"]}
            onChange={setSortOption}
          />

          {/* 필터용 SingleSelector */}
          <SingleSelector
            title="근무 형태"
            options={["전체", "상주", "원격"]}
            onChange={setFilterOption}
          />
        </div>
      </div>

      {/* 필터링 + 정렬된 프로젝트 리스트 */}
      <div className="project-list-container">
        {displayedProjects.map((project) => (
          <FinishedProjectContent
            key={project.projectName}
            content={project}
            onReview={() => handleReview(project.projectID)}
          /> // 평가 버튼 클릭 시 호출
        ))}
      </div>
    </div>
  );
};

export default FinishedProjectPage;
