import React from "react";
import ProjectInfo from "../components/ProjectInfo";
import { useNavigate } from "react-router-dom";

const RegisteredProjects = () => {
  const projects = [
    {
      projectId: 1,
      projectName: "Javascript / jQuery기반 공공기관 홈페이지 프론트엔드 개발",
      duration: 30,
      budget: 4000000,
      workType: 1,
      contractType: 0,
      status: 0,
      registerDate: "20250123",
      categoryName: "소프트웨어/IT",
      skillIdList: [98, 215, 141, 119, 99],
      skillNameList: [
        "Java",
        "jQuery",
        "Oracle",
        "Microsoft SQL Server",
        "JavaScript",
      ],
      locationName: "대전광역시",
      matchingScore: null,
      applied: null,
      similarityScore: null,
      priority: null,
    },
    {
      projectId: 9,
      projectName: "SpringBoot기반 공공기관 웹 구축",
      duration: 35,
      budget: 6416666,
      workType: 1,
      contractType: 0,
      status: 0,
      registerDate: "20250114",
      categoryName: "소프트웨어/IT",
      skillIdList: [11, 143, 112, 98, 41],
      skillNameList: ["Ansible", "PHP", "Make", "Java", "Couch DB"],
      locationName: "대전광역시",
      matchingScore: null,
      applied: null,
      similarityScore: null,
      priority: null,
    },
    {
      projectId: 21,
      projectName: "Flutter/Java 기반 공공기관 사이트 통합 및 고도화 개발",
      duration: 60,
      budget: 12000000,
      workType: 1,
      contractType: 0,
      status: 1,
      registerDate: "20250106",
      categoryName: "소프트웨어/IT",
      skillIdList: [98, 186, 183, 132, 99],
      skillNameList: [
        "Java",
        "Supabase",
        "Spring Boot",
        "Nuxt.js",
        "JavaScript",
      ],
      locationName: "대전광역시",
      matchingScore: null,
      applied: null,
      similarityScore: null,
      priority: null,
    },
  ];

  const navigate = useNavigate();

  const handleRegisterClick = () => {
    navigate("/chat");
  };

  return (
    <div className="registered-project-container">
      <div className="header-container">
        <div className="header-left">
          <h3 className="header">내가 등록한 프로젝트</h3>
          <p>총 {projects.length}개의 등록한 프로젝트가 있습니다.</p>
        </div>
        <div className="header-right">
          <button className="btn-register" onClick={handleRegisterClick}>
            등록하기
          </button>
        </div>
      </div>
      {projects.map((project) => (
        <ProjectInfo
          key={project.projectId}
          content={{
            projectName: project.projectName,
            skillNameList: project.skillNameList,
            locationName: project.locationName,
            registerDate: project.registerDate,
            duration: project.duration,
            budget: project.budget,
            categoryRole: "개발",
            categoryName: project.categoryName,
            status: project.status,
          }}
        />
      ))}
    </div>
  );
};

export default RegisteredProjects;
