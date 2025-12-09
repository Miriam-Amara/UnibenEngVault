/**
 * 
 */

import { useEffect, useState } from "react";

import { fetchAllUsersApi, fetchUsersByDepartmentAndLevelApi } from "../api/users";

export function useUsers() {
  const [ users, setUsers ] = useState([]);
  const [ search, setSearch ] = useState("");
  const [ date, setDate ] = useState("");
  const [ pageNum, setPageNum ] = useState(1);
  const [ pageSize, setPageSize ] = useState(5);
  const [ departmentId, setDepartmentId ] = useState("");
  const [ levelId, setLevelId ] = useState("");

  const fetchAllUsers = async () => {
    try {
      const created_at = date;
      const page_num = pageNum;
      const page_size = pageSize;

      const data = await fetchAllUsersApi({ page_num, page_size, created_at, search });
      setUsers(data)
      console.log("all users: ", data);
    } catch {
        console.log("all users: ", users);
        setUsers([]);
    }
  }

  const fetchFilteredUsers = async () => {
    if (!departmentId && !levelId)
      return;

    try {
      const department_id = departmentId;
      const level_id = levelId;
      const page_num = pageNum;
      const page_size = pageSize;

      const filteredData = await fetchUsersByDepartmentAndLevelApi({
        page_num, page_size, department_id, level_id
      });
      console.log("filteredData: ", filteredData);
      setUsers(filteredData);

    } catch (error) {
      setUsers([]);
      console.log("filteredData: ", users);
      console.error("Error fetching users by department and level: ", error);
    }
  }

  useEffect(() => {
    const timeout = setTimeout(() => {
      fetchAllUsers();
    }, 500) // 500ms

    return () => clearTimeout(timeout);
  }, [date, search]);

  useEffect(() => {
    fetchFilteredUsers();
  }, [departmentId, levelId]);

  const clearFilters = () => {
    setDepartmentId("");
    setLevelId("");
    fetchAllUsers();
  }

  return ({
    users, setUsers,
    search, setSearch,
    date, setDate,
    pageNum, setPageNum,
    pageSize, setPageSize,
    departmentId, setDepartmentId,
    levelId, setLevelId,
    clearFilters, fetchAllUsers
  });
}
