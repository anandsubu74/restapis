async function searchStudents() {
    const searchType = document.getElementById('searchType').value;
    const searchValue = document.getElementById('searchValue').value;

    if (!searchValue) {
        alert("Please enter a search value.");
        return;
    }

    try {
        const response = await fetch(`/student/search?search_type=${searchType}&search_value=${searchValue}`);
        const data = await response.json();

        const tableBody = document.getElementById('resultsTable');
        tableBody.innerHTML = ''; // Clear previous results

        if (response.ok && data.students.length > 0) {
            data.students.forEach(student => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${student.name}</td>
                    <td>${student.major}</td>
                    <td>${student.courses.join(', ')}</td>
                `;
                tableBody.appendChild(row);
            });
        } else {
            tableBody.innerHTML = '<tr><td colspan="3">No students found</td></tr>';
        }
    } catch (error) {
        console.error("Error fetching students:", error);
        alert("An error occurred while searching for students.");
    }
}
