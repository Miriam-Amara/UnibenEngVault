/**
 * 
 */


import { Input } from "../../../components/ui/Input";
import { Select } from "../../../components/ui/Select";
import { Button } from "../../../components/ui/Button";
import refreshIcon from "../../../assets/refresh_icon.png";




export default function Filters({
  pageSize,
  setPageSize,
  date,
  setDate,
  search,
  setSearch,
  departmentId,
  setDepartmentId,
  departments,
  levelId,
  setLevelId,
  levels,
  clearFilters
}) {

  return (
    <div className="flex items-center">

      {/* --------------- PAGINATION PAGE SIZE --------------- */}
      <div className="max-w-18 flex gap-sm mr-5">
        <span>show</span>
        <Input
          type="number"
          name="pageSize"
          value={pageSize}
          onChange={ (e) => {setPageSize(Number(e.target.value));}}
          size="sm"
        />
        <span>entries</span>
      </div>

      {/* --------------- DATE --------------- */}
      <div className="mr-5">
        <Input
          type="date"
          name="date"
          value={date}
          onChange={ (e) => {setDate(e.target.value)} }
          size="sm"
          className="cursor-pointer"
        />
      </div>

      {/* ---------- FILTER BY DEPARTMENT AND LEVEL ---------- */}
      <div className="items-center flex">

        {/* --------------- DEPARTMENT --------------- */}
        <Select
          name="department_id"
          value={ departmentId }
          options={ departments }
          selectType="department"
          onChange={ (e) => {setDepartmentId(e.target.value);}}
          size="sm"
          className="mr-2 cursor-pointer"
        />
        
        {/* --------------- LEVEL --------------- */}
        <Select
          name="level_id"
          value={ levelId }
          options={ levels }
          selectType="level"
          onChange={ (e) => {setLevelId(e.target.value);} }
          size="sm"
          className="cursor-pointer"
        />

        {/* --------------- RESET --------------- */}
        <Button
          type="button"
          variant="icon"
          children={ <img src={ refreshIcon } alt="reset" className="w-50"/>}
          onClick={ clearFilters }
        />
      </div>

      {/* --------------- SEARCH --------------- */}
      <div className="ml-auto">
        <Input
          type="text"
          name="search"
          value={ search }
          placeholder="Search user..."
          onChange={ (e) => {setSearch(e.target.value)} }
          className="rounded-10 max-w-19"
        />
      </div>    
    </div>
  );
}
