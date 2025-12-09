/**
 * 
 */

import { useEffect, useState } from "react";

import { fetchAllDepartmentsApi } from "../api/departments";


export function useSelectDepartments() {
  const [ departments, setDepartments ] = useState([]);

  const fetchDepartments = async (params={}) => {
    try {
      const data = await fetchAllDepartmentsApi(params);
      const options = data?.map((department) => ({
        value: department.id,
        label: department.dept_name
      })) ?? [];

      setDepartments(options);
    } catch (error) {
      console.error("Error fetching departments", error);
    }
  };

  useEffect(() => {fetchDepartments();}, []);

  return departments
}

