import React, { useState, useEffect } from "react";
import ProjectInfo from "../components/ProjectInfo";
import SingleSelector from "../components/SingleSelector";
import MultiSelector from "../components/MultiSelector";
import SwitchButton from "../components/SwitchButton";

const SearchProjectPage = () => {
  // 프로젝트 데이터
  const [projects, setProjects] = useState([
    {
      projectId: 101,
      projectName: "AI 기반 추천 시스템 개발",
      duration: 6,
      budget: 5000000,
      workType: 1,
      contractType: 0,
      status: 0,
      registerDate: "20250127",
      categoryName: "소프트웨어/IT",
      skillIdList: [1, 2, 3],
      skillNameList: ["Python", "Machine Learning", "Deep Learning"],
      locationName: "서울시 강남구",
    },
    {
      projectId: 102,
      projectName: "프리랜서 여행 플랫폼 프론트엔드 개발",
      duration: 30,
      budget: 3000000,
      workType: 1,
      contractType: 0,
      status: 1,
      registerDate: "20250212",
      categoryName: "소매/소비자",
      skillIdList: [4, 5],
      skillNameList: ["React", "TypeScript"],
      locationName: "서울시 종로구",
    },
  ]);

  // 필터 상태
  const [showOnlyRecruiting, setShowOnlyRecruiting] = useState(false);
  const [sortOption, setSortOption] = useState("최신순");
  const [categoryFilterOption, setCategoryFilterOption] = useState("전체");
  const [displayedProjects, setDisplayedProjects] = useState([]);

  // 필터링 & 정렬 기능 적용
  useEffect(() => {
    let updatedProjects = [...projects];

    // 모집 중인 프로젝트만 보기 기능 적용
    if (showOnlyRecruiting) {
      updatedProjects = updatedProjects.filter((project) => !project.status);
    }

    // 직무/직군 필터링 적용
    if (categoryFilterOption !== "전체") {
      updatedProjects = updatedProjects.filter(
        (project) => project.categoryName === categoryFilterOption
      );
    }

    // // 스킬 필터링 적용
    // if (categoryFilterOption !== "전체") {
    //   updatedProjects = updatedProjects.filter(
    //     (project) => project.categoryName === categoryFilterOption
    //   );
    // }

    // 정렬 적용 (최신순 / 추천순 / 금액 많은순)
    if (sortOption === "최신순") {
      updatedProjects.sort((a, b) =>
        b.registerDate.localeCompare(a.registerDate)
      );
      // } else if (sortOption === "추천순") {
      //   updatedProjects.sort((a, b) => b.feedbackScore - a.feedbackScore);
    } else if (sortOption === "금액 많은순") {
      updatedProjects.sort((a, b) => b.budget - a.budget);
    }

    setDisplayedProjects(updatedProjects);
  }, [sortOption, categoryFilterOption, showOnlyRecruiting, projects]); // 옵션(정렬/필터/스위치) 변경 시 실행

  return (
    <div>
      {/* 필터 UI */}
      <div>
        <MultiSelector
          title="직군 선택"
          options={[
            "전체",
            "소프트웨어/IT",
            "금융",
            "소매/소비자",
            "미디어/광고",
            "제조업",
            "운송/공급망",
            "정부",
            "에너지",
            "헬스케어",
            "교육",
          ]}
          onChange={setCategoryFilterOption}
        />
        <SwitchButton
          text="모집 중인 프로젝트만 표시"
          onChange={setShowOnlyRecruiting}
        />

        <SingleSelector
          title="정렬"
          options={["최신순", "금액 많은순"]}
          onChange={setSortOption}
        />
      </div>

      {/* 필터링된 프로젝트 리스트 */}
      {displayedProjects.map((project) => (
        <ProjectInfo
          key={project.projectId}
          projectinfo1={{
            title: project.projectName,
            skills: project.skillNameList,
            where: project.locationName,
            start_day: project.registerDate,
            day: project.duration,
            pay: project.budget,
            job: "개발",
            category: project.categoryName,
            state: project.status,
          }}
        />
      ))}
    </div>
  );
};

export default SearchProjectPage;
