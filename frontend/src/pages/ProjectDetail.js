import React from "react";
import SimilarProject from "../components/SimilarProject";
import ProjectInfo from "../components/ProjectInfo";
import "../style/ProjectDetail.css";

const ProjectDetail = () => {
  const project = {
    projectId: 570,
    projectName: "위치 기반 공간 사용 예약/결제 플랫폼 개선 및 추가 개발",
    duration: 30,
    budget: 15000000,
    workType: 0,
    contractType: 1,
    priority: 1,
    projectContent:
      "프로젝트 개요 :\n- 럭스테이는 앱스토어, 구글 플레이 스토어에서 '럭스테이'로 검색하면 나오면 앱이며 현재 운영중에 있습니다.\n\n진행 일정 :\n- 미팅 시 업체와 협의할 예정입니다. 과업 범위를 검토하시고 소요 기간을 알려주시면 좋습니다.\n\n프로젝트의 현재 상황 :\n- 운영 중 필요한 신규 기능 및 기존 기능의 수정이 필요하여 개선 의뢰를 드리려 합니다.\n- 코드 내 주석은 작성되어 있으나 API 명세서, DB 설계도는 없습니다.\n\n필요 요소 :\n- 기존 소스 코드 검토\n- 기능 개선/신규 기능에 대한 상세 기획\n- UI 디자인\n- 모바일앱 프런트엔드 개발\n- 백엔드 개발\n- 관리자페이지 추가 개발\n\n개발 환경/언어 :\n- Node.js\n- flutter\n- vue.js\n- MySQL\n- AWS\n\n과업 범위 :\n- 첨부된 엑셀파일 내 노락색으로 표시된 항목들이 이번 프로젝트의 과업 범위입니다.\n\n산출물 :\n- 기획 문서\n- 디자인 원본\n- 소스 코드 원본\n\n지원 시 참고 사항 :\n- 기재된 예산 안에서 가능한 과업 범위를 역으로 제안해주시기 바랍니다.\n- 기획/디자인을 제외한 개발 파트만 수행하는 방식으로도 지원 가능합니다. 개발만 진행 시 견적은 별도로 알려주세요.\n- 풀스텍 개발자 1분과 계약하는 방식도 가능합니다.\n- 프런트엔드 1분 + 백엔드 1분으로 구성된 개발팀/업체와 계약하는 방식도 가능합니다.",
    status: 0,
    registerDate: "20250124",
    categoryId: 0,
    categoryName: "소프트웨어/IT",
    skillList: ["MySQL", "Vue.js", "Strapi", "OpenStack", "Node.js"],
    companyId: 2616,
    companyName: "da******",
    locationName: "세종특별자치시",
  };

  const skillList = project.skillList || []; // skillList가 없으면 빈 배열 할당
  const skillNameList = skillList.map((skill) => skill.name) || []; // skillNameList 생성

  const projects = [
    {
      projectId: 101,
      projectName: "Python 개발 프로젝트",
      duration: 30,
      budget: 5000000,
      workType: 1,
      contractType: 0,
      status: 0,
      registerDate: "20250125",
      categoryName: "IT•정보통신업",
      skillIdList: [1, 2, 3],
      skillNameList: ["Python", "Django", "API"],
      locationName: "서울특별시 강남구",
      similarityScore: 15,
    },
    {
      projectId: 102,
      projectName: "Java 백엔드 개발",
      duration: 60,
      budget: 10000000,
      workType: 0,
      contractType: 1,
      status: 0,
      registerDate: "20250120",
      categoryName: "IT•정보통신업",
      skillIdList: [4, 5, 6],
      skillNameList: ["Java", "Spring", "REST"],
      locationName: "서울특별시 서초구",
      similarityScore: 12,
    },
    {
      projectId: 101,
      projectName: "Python 개발 프로젝트",
      duration: 30,
      budget: 5000000,
      workType: 1,
      contractType: 0,
      status: 0,
      registerDate: "20250125",
      categoryName: "IT•정보통신업",
      skillIdList: [1, 2, 3],
      skillNameList: ["Python", "Django", "API"],
      locationName: "서울특별시 강남구",
      similarityScore: 15,
    },
  ];
  return (
    <div className="container2">
      <div className="left-card">
        <ProjectInfo content={project} />
      </div>

      <div className="right-cards">
        <div className="top-card">
          <div className="plzbold">
            <strong>지금 보는 프로젝트에 관심이 있나요?</strong>
          </div>
          <div className="plzblack">프로젝트에 지원해보세요!</div>
          <div className="button-container2">
            <button className="edit-button">지원하기</button>
          </div>
        </div>
        <div className="bottom-card">
          <SimilarProject projects={projects} />
        </div>
      </div>
    </div>
  );
};
export default ProjectDetail;
