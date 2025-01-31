import React, { useState } from "react";
import FreelancerInfo from "../components/FreelancerInfo";
import "../style/RecommendFreelancer.css";
import profile1 from "../assets/profile_example1.jpg";
import profile2 from "../assets/profile_example2.jpg";
import profile3 from "../assets/profile_example3.jpg";

const RecommendFreelancer = () => {
  const [search, setSearch] = useState("");
  const [filterRole, setFilterRole] = useState("");
  const [filterWorkType, setFilterWorkType] = useState("");
  const [filterSkillList, setFilterSkillList] = useState("");

  const freelancers = [
    {
      photo: profile1,
      freelancerId: 122,
      freelancerName: "희수희수야",
      workExp: "7년",
      workType: "원격",
      role: "백엔드 개발자",
      freelancerContent:
        "27년 차 Java 개발자로, 백엔드와 프론트엔드 개발에 모두 능숙합니다. 데이터베이스 설계 및 관리 경험이 풍부하며, 앱 개발과 배포까지 전 과정을 주도한 경험이 있습니다.",
      locationName: "양산",
      categoryList: ["IT•정보통신업", "건설업"],
      skillList: [
        { skillName: "Java", skillScore: 4.5 },
        { skillName: "Spring Boot", skillScore: 4 },
        { skillName: "jQuery", skillScore: 3.5 },
        { skillName: "SQL", skillScore: 4.5 },
        { skillName: "AJAX", skillScore: 3 },
        { skillName: "JSP", skillScore: 4 },
      ],
      feedbackCount: 12,
      expertise: 4.2,
      proactiveness: 4.3,
      punctuality: 4.1,
      maintainability: 4.0,
      communication: 4.4,
      matchingScore: 90,
      applied: 1,
    },
    {
      photo: profile2,
      freelancerId: 123,
      freelancerName: "박왕균이",
      workExp: "3년",
      workType: "원격",
      role: "프론트엔드 개발자",
      freelancerContent:
        "웹 애플리케이션 개발, 클라우드 관리 시스템 개발, 모바일 앱 개발, 금융 백엔드 시스템 개발, 게임 클라이언트/서버 개발 등 다양한 업무의 개발 경험이 있으며, 서비스 운영 경험을 다년간 지니고 있는 시니어 개발자.",
      locationName: "서울",
      categoryList: ["제조업", "IT•정보통신업"],
      skillList: [
        { skillName: "Python", skillScore: 5 },
        { skillName: "PyTorch", skillScore: 4 },
        { skillName: "Tensorflow", skillScore: 4.5 },
        { skillName: "HTML", skillScore: 2 },
        { skillName: "Vue.js", skillScore: 4 },
        { skillName: "CSS", skillScore: 3.5 },
      ],
      feedbackCount: 18,
      expertise: 4.7,
      proactiveness: 4.8,
      punctuality: 4.6,
      maintainability: 4.5,
      communication: 4.7,
      matchingScore: 60,
      applied: 0,
    },
    {
      photo: profile3,
      freelancerId: 124,
      freelancerName: "성택의선택",
      workExp: "5년",
      workType: "대면",
      role: "백엔드 개발자",
      freelancerContent:
        "혁신적인 것을 더 많이 만들 수 있는 다재다능한 능력을 가진 경험이 풍부한 베테랑 개발자입니다. 보다 효율적이고 신속적인 접근으로 문제 해결을 중심으로 역할을 수행하고 있습니다.",
      locationName: "서울",
      categoryList: ["제조업", "IT•정보통신업"],
      skillList: [
        { skillName: "Java", skillScore: 4 },
        { skillName: "Spring Boot", skillScore: 4.5 },
        { skillName: "jQuery", skillScore: 3.5 },
        { skillName: "SQL", skillScore: 4 },
        { skillName: "AJAX", skillScore: 3 },
        { skillName: "JSP", skillScore: 1 },
      ],
      feedbackCount: 18,
      expertise: 4.7,
      proactiveness: 4.8,
      punctuality: 4.6,
      maintainability: 4.5,
      communication: 4.7,
      matchingScore: 40,
      applied: 1,
    },
  ];

  freelancers.forEach((freelancer) => {
    const {
      expertise,
      proactiveness,
      punctuality,
      maintainability,
      communication,
    } = freelancer;
    freelancer.feedbackScore =
      (expertise +
        proactiveness +
        punctuality +
        maintainability +
        communication) /
      5;
  });

  const filteredFreelancers = freelancers.filter((freelancer) => {
    return (
      freelancer.freelancerName.includes(search) &&
      (!filterRole || freelancer.role === filterRole) &&
      (!filterWorkType || freelancer.workType === filterWorkType) &&
      (!filterSkillList || freelancer.skillList === filterSkillList)
    );
  });

  return (
    <div className="freelancer-list-container">
      <div className="header-container">
        <h3 className="header">추천 프리랜서 리스트</h3>
        <p>총 {freelancers.length}명의 프리랜서가 있습니다.</p>
      </div>
      <div className="filters">
        <select onChange={(e) => setFilterRole(e.target.value)}>
          <option value="">직무</option>
          <option value="백엔드 개발자">백엔드 개발자</option>
          <option value="프론트엔드 개발자">프론트엔드 개발자</option>
        </select>
        <select onChange={(e) => setFilterWorkType(e.target.value)}>
          <option value="">근무 형태</option>
          <option value="대면">대면</option>
          <option value="원격">원격</option>
        </select>
        <select onChange={(e) => setFilterSkillList(e.target.value)}>
          <option value="">스킬</option>
          <option value="Java">Java</option>
          <option value="SQL">SQL</option>
        </select>
        <input
          type="text"
          placeholder="검색"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
      </div>

      <div className="freelancers">
        {filteredFreelancers.map((freelancer) => (
          <FreelancerInfo
            key={freelancer.freelancerId}
            freelancerInfo={freelancer}
            pageType="recommend"
          />
        ))}
      </div>
    </div>
  );
};

export default RecommendFreelancer;
