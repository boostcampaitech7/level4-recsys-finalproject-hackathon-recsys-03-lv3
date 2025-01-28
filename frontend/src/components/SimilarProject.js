import React from "react";
import "../style/SimilarProject.css";

const SimilarProject = () => {
  const projects = [
    {
      title: "기업 - 프리랜서 매칭 플랫폼 프론트엔드 개발",
      description: "HTML, CSS, Javascript, Vue.js를 사용하는 프로젝트",
      tags: ["HTML", "CSS", "Javascript", "Vue.js"],
    },
    {
      title: "기업 - 프리랜서 매칭 플랫폼 백엔드 개발",
      description: "Spring Boot와 Java를 사용하는 프로젝트",
      tags: ["Java", "Spring Boot"],
    },
    {
      title: "기업 - AI 기반 추천 시스템",
      description: "Python과 TensorFlow를 사용하는 프로젝트",
      tags: ["Python", "TensorFlow"],
    },
    {
      title: "스타트업 - 모바일 앱 개발",
      description: "React Native를 사용하는 프로젝트",
      tags: ["React Native"],
    },
  ];

  return (
    <div
      id="carouselExample"
      className="carousel slide"
      data-bs-ride="carousel"
    >
      <div className="carousel-inner">
        {/* 프로젝트 데이터를 두 개씩 묶어서 렌더링 */}
        {projects.reduce((acc, project, index) => {
          if (index % 2 === 0) {
            const slide = (
              <div
                className={`carousel-item ${index === 0 ? "active" : ""}`}
                key={index}
              >
                <div className="row">
                  {/* 첫 번째 카드 */}
                  <div className="col-md-12">
                    <div className="card p-3">
                      <h5>{projects[index].title}</h5>
                      <p>{projects[index].description}</p>
                      <div>
                        {projects[index].tags.map((tag, i) => (
                          <span key={i} className="badge bg-secondary me-2">
                            {tag}
                          </span>
                        ))}
                      </div>
                    </div>
                  </div>
                  {/* 두 번째 카드 (데이터가 존재하는 경우) */}
                  {projects[index + 1] && (
                    <div className="col-md-12">
                      <div className="card p-3">
                        <h5>{projects[index + 1].title}</h5>
                        <p>{projects[index + 1].description}</p>
                        <div>
                          {projects[index + 1].tags.map((tag, i) => (
                            <span key={i} className="badge bg-secondary me-2">
                              {tag}
                            </span>
                          ))}
                        </div>
                      </div>
                    </div>
                  )}
                </div>
              </div>
            );
            acc.push(slide);
          }
          return acc;
        }, [])}
      </div>
      <button
        className="carousel-control-prev"
        type="button"
        data-bs-target="#carouselExample"
        data-bs-slide="prev"
      >
        <span className="carousel-control-prev-icon" aria-hidden="true"></span>
        <span className="visually-hidden">Previous</span>
      </button>
      <button
        className="carousel-control-next"
        type="button"
        data-bs-target="#carouselExample"
        data-bs-slide="next"
      >
        <span className="carousel-control-next-icon" aria-hidden="true"></span>
        <span className="visually-hidden">Next</span>
      </button>
    </div>
  );
};

export default SimilarProject;
