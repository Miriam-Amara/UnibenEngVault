/**
 * 
 */

import { useEffect, useState } from "react";
import { fetchAllLevelsApi } from "../api/levels";



export function useSelectLevels() {
  const [ levels, setLevels ] = useState([]);

  const fetchLevels = async (params={}) => {
    try {
      const data = await fetchAllLevelsApi(params);
      const options = data?.map((level) => ({
        value: level.id,
        label: level.level_name
      })) ?? [];

      setLevels(options ?? []);
    } catch (error) {
      console.error("Error fetching levels", error);
    }
  };

  useEffect(() => {fetchLevels();}, []);

  return levels;
}


export function useLevels() {
  const [ levels, setLevels ] = useState([]);

  const fetchLevels = async (params={}) => {
    try {
      const data = fetchAllLevelsApi(params);
      setLevels(data ?? []);
    } catch (error) {
      console.error("Error fetching levels", error);
    }
  };

  return [ levels, fetchLevels ];
}
