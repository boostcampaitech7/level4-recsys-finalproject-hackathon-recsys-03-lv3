import React from "react";
import FreelancerInfo from "../components/FreelancerInfo";
import "../style/SearchFreelancer.css";
import profile1 from "../assets/profile_example1.jpg";
import profile2 from "../assets/profile_example2.jpg";
import profile3 from "../assets/profile_example3.jpg";

const SearchFreelancer = () => {
  const freelancers = [
    {
      photo: profile1,
      name: "희수희수야",
      feedbackscore: 5.0,
      feedbackcount: 12,
      role: "백엔드 개발자",
      workexp: "7년",
      worktype: "원격",
      location: "양산",
      content:
        "27년 차 Java 개발자로, 백엔드와 프론트엔드 개발에 모두 능숙합니다. 데이터베이스 설계 및 관리 경험이 풍부하며, 앱 개발과 배포까지 전 과정을 주도한 경험이 있습니다.",
      skills: [
        { skill: "Java", score: 4.5 },
        { skill: "Spring Boot", score: 4 },
        { skill: "jQuery", score: 3.5 },
        { skill: "SQL", score: 4.5 },
        { skill: "AJAX", score: 3 },
        { skill: "JSP", score: 4 },
      ],
      radarData: [5, 5, 5, 5, 5],
    },
    {
      photo: profile2,
      name: "박왕균이",
      feedbackscore: 4.7,
      feedbackcount: 18,
      role: "프론트엔드 개발자",
      workexp: "3년",
      worktype: "원격",
      location: "서울",
      content:
        "웹 애플리케이션 개발, 클라우드 관리 시스템 개발, 모바일 앱 개발, 금융 백엔드 시스템 개발, 게임 클라이언트/서버 개발 등 다양한 업무의 개발 경험이 있으며, 서비스 운영 경험을 다년간 지니고 있는 시니어 개발자.",
      skills: [
        { skill: "Python", score: 5 },
        { skill: "PyTorch", score: 4 },
        { skill: "Tensorflow", score: 4.5 },
        { skill: "HTML", score: 2 },
        { skill: "Vue.js", score: 4 },
        { skill: "CSS", score: 3.5 },
      ],
      radarData: [4, 5, 4, 4, 4],
    },
    {
      photo: profile3,
      name: "성택이선택",
      feedbackscore: 4.8,
      feedbackcount: 15,
      role: "백엔드 개발자",
      workexp: "5년",
      worktype: "대면",
      location: "서울",
      content:
        "혁신적인 것을 더 많이 만들 수 있는 다재다능한 능력을 가진 경험이 풍부한 베테랑 개발자입니다. 보다 효율적이고 신속적인 접근으로 문제 해결을 중심으로 역할을 수행하고 있습니다.",
      skills: [
        { skill: "Java", score: 4 },
        { skill: "Spring Boot", score: 4.5 },
        { skill: "jQuery", score: 3.5 },
        { skill: "SQL", score: 4 },
        { skill: "AJAX", score: 3 },
        { skill: "JSP", score: 1 },
      ],
      radarData: [4, 4, 4, 5, 4],
    },
  ];

  return (
    <div className="search-freelancer-container">
      <div className="header-container">
        <h3 className="header">프리랜서 리스트</h3>
        <p>총 {freelancers.length}명의 프리랜서가 있습니다.</p>
      </div>
      {freelancers.map((freelancer, index) => (
        <div key={index} className="card-container">
          <FreelancerInfo profile={freelancer} className="card" />
        </div>
      ))}
    </div>
  );
};

export default SearchFreelancer;
