import { useContext } from "react";
import { CalendarContext, EventContext, TaskContext } from "../context/CalendarEventTaskContext"
import { Received_InviteContext, Sent_InviteContext } from "../context/InviteContext"
import { CollaborationContext } from "../context/CollaborationContext";

const createUseContextHook = (Context, contextName) => {
    return () => {
            const context = useContext(Context)
            if (!context) {
                throw new Error(`use${contextName} must be used within a ${contextName}Provider`)
            }
            return context
    }
}

export const useCalendarContext = createUseContextHook(CalendarContext, 'Calendar')
export const useTaskContext= createUseContextHook(TaskContext, 'Task')
export const useEventContext = createUseContextHook(EventContext, 'Event')
export const useSentInviteContext = createUseContextHook(Sent_InviteContext, 'Invite')
export const useReceivedInviteContext = createUseContextHook(Received_InviteContext, 'Invite')
export const useCollaborationContext = createUseContextHook(CollaborationContext, 'Collaboration')
