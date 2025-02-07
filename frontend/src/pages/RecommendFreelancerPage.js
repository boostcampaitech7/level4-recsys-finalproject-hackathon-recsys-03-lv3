import React, { useEffect, useState } from "react";
import { useParams, useLocation } from "react-router-dom";
import axios from "axios";
import FreelancerInfo from "../components/FreelancerInfo";
import MultiSelector from "../components/MultiSelector";
import SingleSelector from "../components/SingleSelector";
import SwitchButton from "../components/SwitchButton";
import "../style/SearchPages.css";
import profile1 from "../assets/profile_example1.jpg";
import profile2 from "../assets/profile_example2.jpg";
import profile3 from "../assets/profile_example3.jpg";

const API_BASE_URL = `${process.env.REACT_APP_BASE_URL}/api/mymony/prestart-project`;

const RecommendFreelancer = () => {
  const { projectId } = useParams(); // URL에서 projectId를 가져옴
  const location = useLocation();
  const { projectName } = location.state || {};

  const [freelancers, setFreelancers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const roleList = ["백엔드 개발자", "프론트엔드 개발자", "풀스택 개발자"];
  const skillList = JSON.parse(sessionStorage.getItem("skill"), "[]").map(
    (skill) => skill.skillName
  );

  const [filterRoles, setFilterRoles] = useState([]);
  const [filterWorkType, setFilterWorkType] = useState("근무 형태");
  const [filterSkillList, setFilterSkillList] = useState(skillList);
  const [sortOption, setSortOption] = useState("최신순");
  const [showOnlyApplied, setShowOnlyApplied] = useState(false);

  const userId = sessionStorage.getItem("userId");

  useEffect(() => {
    const token = sessionStorage.getItem("token");

    if (!token) {
      setError("인증 토큰이 없습니다. 로그인 후 이용해주세요.");
      setLoading(false);
      return;
    }

    const fetchFreelancers = async () => {
      try {
        const response = await axios.get(`${API_BASE_URL}/${projectId}`, {
          headers: {
            Accept: "application/json",
            Authorization: `Bearer ${token}`,
          },
        });
        setFreelancers(response.data);
      } catch (error) {
        console.error("프리랜서 데이터를 불러오는 데 실패했습니다:", error);
        setError("프리랜서 데이터를 불러오는 데 실패했습니다.");
      } finally {
        setLoading(false);
      }
    };

    fetchFreelancers();
  }, []);

  if (loading) return <div>로딩 중...</div>;
  if (error) return <div className="error-message">{error}</div>;

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

  // 필터링 로직
  const filteredFreelancers = freelancers
    .filter((freelancer) => {
      return (
        (!showOnlyApplied || freelancer.applied === 1) &&
        (filterRoles.length === 0 || filterRoles.includes(freelancer.role)) &&
        (filterWorkType === "근무 형태" ||
          (freelancer.workType === 0 ? "대면" : "원격") === filterWorkType) &&
        freelancer.skillList.some((skill) => filterSkillList.includes(skill))
      );
    })
    .sort((a, b) => {
      // 정렬 로직
      if (sortOption === "최신순") return b.freelancerId - a.freelancerId;
      if (sortOption === "매칭 점수 높은순")
        return b.matchingScore - a.matchingScore;
      return 0;
    });

  const resetFilters = () => {
    setFilterRoles(roleList);
    setFilterWorkType("근무 형태");
    setFilterSkillList(skillList);
    setSortOption("최신순");
    setShowOnlyApplied(false);
  };

  return (
    <div className="freelancer-list-container">
      <div className="header-container">
        <p className="fw-bold mt-3">[{projectName}]</p>
        <h3 className="header">추천 프리랜서 리스트</h3>
        <p>총 {filteredFreelancers.length}명의 프리랜서가 있습니다.</p>
      </div>
      <div className="filters">
        <div className="filter-group-left">
          {/* 직군 필터 */}
          <MultiSelector
            title="직군/직무"
            options={roleList}
            onChange={setFilterRoles}
            value={filterRoles}
          />

          {/* 근무 형태 필터 */}
          <SingleSelector
            title="근무 형태"
            options={["근무 형태", "원격", "대면"]}
            onChange={setFilterWorkType}
            value={filterWorkType}
          />

          {/* 스킬 필터 */}
          <MultiSelector
            title="스킬"
            options={skillList}
            onChange={setFilterSkillList}
            value={filterSkillList}
          />

          {/* 필터 초기화 버튼 */}
          <button className="reset-button" onClick={resetFilters}>
            <i className="bi bi-arrow-counterclockwise"></i> 필터 초기화
          </button>
        </div>

        {/* 정렬 옵션 */}
        <div className="filter-group-right">
          <SwitchButton
            text="지원한 사람만 보기"
            checked={showOnlyApplied}
            onChange={setShowOnlyApplied}
          />
          <SingleSelector
            title="정렬 기준"
            options={["최신순", "매칭 점수 높은순"]}
            onChange={setSortOption}
            value={sortOption}
          />
        </div>
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
