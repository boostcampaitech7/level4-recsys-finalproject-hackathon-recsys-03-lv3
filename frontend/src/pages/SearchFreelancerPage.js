import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import FreelancerInfo from "../components/FreelancerInfo";
import MultiSelector from "../components/MultiSelector";
import SingleSelector from "../components/SingleSelector";
import "../style/SearchPages.css";
import profile1 from "../assets/profile_example1.jpg";
import profile2 from "../assets/profile_example2.jpg";
import profile3 from "../assets/profile_example3.jpg";

const API_BASE_URL = `${process.env.REACT_APP_BASE_URL}/api/resource`;

const SearchFreelancer = () => {
  const navigate = useNavigate();

  const [freelancers, setFreelancers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const roleList = ["백엔드 개발자", "프론트엔드 개발자", "풀스택 개발자"];
  const skillList = JSON.parse(sessionStorage.getItem("skill"), "[]").map(
    (skill) => skill.skillName
  );

  const [filterRoles, setFilterRoles] = useState(roleList);
  const [filterWorkType, setFilterWorkType] = useState("근무 형태");
  const [filterSkillList, setFilterSkillList] = useState(skillList);
  const [sortOption, setSortOption] = useState("피드백 점수 높은순");

  // 프리랜서를 클릭하면 freelancerId만 전달
  const handleFreelancerClick = (freelancerId) => {
    navigate("/freelancer-detail", { state: { freelancerId } });
  };

  useEffect(() => {
    const token = sessionStorage.getItem("token");

    if (!token) {
      setError("인증 토큰이 없습니다. 로그인 후 이용해주세요.");
      setLoading(false);
      return;
    }

    const fetchFreelancers = async () => {
      try {
        const response = await axios.get(API_BASE_URL, {
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
        filterRoles.includes(freelancer.role) &&
        (filterWorkType === "근무 형태" ||
          (freelancer.workType === 0 ? "대면" : "원격") === filterWorkType) &&
        freelancer.skillList.some((skill) => filterSkillList.includes(skill))
      );
    })
    .sort((a, b) => {
      // 정렬 로직
      if (sortOption === "피드백 점수 높은순")
        return b.feedbackScore - a.feedbackScore;
      if (sortOption === "매칭 점수 높은순")
        return b.matchingScore - a.matchingScore;
      return 0;
    });

  const resetFilters = () => {
    setFilterRoles(roleList);
    setFilterWorkType("근무 형태");
    setFilterSkillList(skillList);
    setSortOption("피드백 점수 높은순");
  };

  // console.log(filteredFreelancers);
  // console.log(freelancers);

  return (
    <div className="search-freelancer-container">
      <div className="header-container">
        <h3 className="header">프리랜서 리스트</h3>
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
          <SingleSelector
            title="정렬 기준"
            options={["피드백 점수 높은순", "매칭 점수 높은순"]}
            onChange={setSortOption}
            value={sortOption}
          />
        </div>
      </div>

      {/* 필터링된 프리랜서 리스트 */}
      {filteredFreelancers.map((freelancer) => (
        <div
          key={freelancer.freelancerId}
          onClick={() => handleFreelancerClick(freelancer.freelancerId)}
          style={{ cursor: "pointer" }}
        >
          <FreelancerInfo
            key={freelancer.freelancerId}
            freelancerInfo={freelancer}
            pageType="search"
          />
        </div>
      ))}
    </div>
  );
};

export default SearchFreelancer;
